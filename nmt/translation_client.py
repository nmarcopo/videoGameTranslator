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
        '''
            Load translation model and sentencepiece models
        '''
        imported = tf.saved_model.load(export_dir)
        self._translate_fn = imported.signatures["serving_default"]
        sp_jpn_model_path = os.path.join(export_dir, "assets.extra", "sp.jpn.model")
        sp_eng_model_path = os.path.join(export_dir, "assets.extra", "sp.eng.model")
        self.jpn_tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_jpn_model_path)
        self.eng_tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_eng_model_path)


    def translate(self, texts):
        """
            Translate text with on-fly tokenization
        """
        # Skip empty string
        if texts[0] == '':
            return ['']
        inputs = self.tokenize(texts)
        outputs = self._translate_fn(**inputs)
        return self.detokenize(outputs)

    def tokenize(self, texts):
        '''
            Tokenize list of sentences
        '''
        all_tokens = []
        lengths = []
        max_length = 0

        # Tokenize each sentences
        for text in texts:
            tokens, _ = self.jpn_tokenizer.tokenize(text)
            length = len(tokens)
            all_tokens.append(tokens)
            lengths.append(length)
            max_length = max(max_length, length)
        
        # Pad all sentences to same length
        for tokens, length in zip(all_tokens, lengths):
            if length < max_length:
                tokens += [""] * (max_length - length)
        
        inputs = {
            "tokens": tf.constant(all_tokens, dtype=tf.string),
            "length": tf.constant(lengths, dtype=tf.int32)
            }
        return inputs

    def detokenize(self, outputs):
        '''
            Detokinze output by reading in only the text
        '''
        texts = []
        for tokens, length in zip(outputs["tokens"].numpy(), outputs["length"].numpy()):
            [tokens], [length] = tokens, length
            tokens = tokens[:length].tolist()
            texts.append(self.eng_tokenizer.detokenize(tokens))
        return texts    


if __name__ == "__main__":
    '''
        For CLI usage
    '''
    parser = argparse.ArgumentParser(description="Translation client")
    parser.add_argument("--export_dir", default="translation_model", help="Saved model directory")
    args = parser.parse_args()

    translator = Translator(args.export_dir)

    while True:
        text = input("Source: ")
        output = translator.translate([text])
        output_str = '\n'.join(output)
        print(f"Target: {output_str}")
        print("")
