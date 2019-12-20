'''
    Create sentencepiece model from input
'''

import sentencepiece as spm
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="sentencepiece trainer")
    parser.add_argument("--vocab-size", default="16000")
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--model-name", required=True, help="Named of the output setencepiece model")

    args = parser.parse_args()

    spm.SentencePieceTrainer.Train(f'--input={args.input_file} --model_prefix={args.model_name} \
                                     --vocab_size={args.vocab_size}')