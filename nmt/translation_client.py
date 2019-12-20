'''
   Serving Translation model
'''


import argparse
import os

import tensorflow as tf
import tensorflow_addons as tfa 

import pyonmttok


class Translator(object):

  def __init__(self, export_dir):
    imported = tf.saved_model.load(export_dir)
    self._translate_fn = imported.signatures["serving_default"]
    sp_jp_model_path = os.path.join(export_dir, "assets.extra", "sp.jpn.model")
    sp_en_model_path = os.path.join(export_dir, "assets.extra", "sp.eng.model")
    self._jp_tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_jp_model_path)
    self._en_tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_en_model_path)


  def translate(self, texts):
    """Translates a batch of texts."""
    inputs = self._preprocess(texts)
    outputs = self._translate_fn(**inputs)
    return self._postprocess(outputs)

  def _preprocess(self, texts):
    all_tokens = []
    lengths = []
    max_length = 0
    for text in texts:
      tokens, _ = self._jp_tokenizer.tokenize(text)
      length = len(tokens)
      all_tokens.append(tokens)
      lengths.append(length)
      max_length = max(max_length, length)
    for tokens, length in zip(all_tokens, lengths):
      if length < max_length:
        tokens += [""] * (max_length - length)
    inputs = {
        "tokens": tf.constant(all_tokens, dtype=tf.string),
        "length": tf.constant(lengths, dtype=tf.int32)}
    return inputs

  def _postprocess(self, outputs):
    texts = []
    for tokens, length in zip(outputs["tokens"].numpy(), outputs["length"].numpy()):
      tokens = tokens[0][:length[0]].tolist()
      texts.append(self._en_tokenizer.detokenize(tokens))
    return texts


def main():
  parser = argparse.ArgumentParser(description="Translation client")
  parser.add_argument("--export_dir", default="translation_model", help="Saved model directory")
  args = parser.parse_args()

  translator = Translator(args.export_dir)

  while True:
    text = input("Source: ")
    if text == '':
        continue
    output = translator.translate([text])
    print("Target: %s" % output[0])
    print(output[0])
    print("")


if __name__ == "__main__":
  main()
