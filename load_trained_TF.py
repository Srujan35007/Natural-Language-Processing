import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
from argparse import ArgumentParser as AP 
import tensorflow as tf 
from tensorflow.keras import models, layers
from tokenizer import Tokenizer
from curtsies.fmtfuncs import bold, red, yellow, blue, cyan
import numpy as np 
print(f"Imports complete")

def pad_sequence(sequence, max_len=20, pad_type='pre'):
    if len(sequence) < max_len:
        if pad_type == 'pre':
            return [0]*(max_len-len(sequence)) + sequence
        elif pad_type == 'post':
            return sequence + [0]*(max_len-len(sequence))
        else:
            print(f"only 'pre' or 'post' padding allowed.")
            exit()
    elif len(sequence) >= max_len:
        return sequence[:max_len]

parser = AP()
parser.add_argument("saved_model_path")
parser.add_argument("saved_tokenizer_path")
args = parser.parse_args()

model = models.load_model(args.saved_model_path)
tokenizer = Tokenizer(load_path=args.saved_tokenizer_path)
print(blue("Trained model and tokenizer loaded"))

max_seq_len = tokenizer.max_sequence_len
print(red("type quit() to quit\n"))
while True:
    MAX_WORDS = 20
    seed_text = input(bold(cyan(">> "))).lower().strip()
    if seed_text == 'quit()':
        exit()
    else:
        pass
    seed_text_tok = tokenizer.tokenize(seed_text)
    len_seed_text = len(seed_text_tok)
    for _ in range(MAX_WORDS-len_seed_text):
        out = np.argmax(model.predict([pad_sequence(seed_text_tok, max_len=max_seq_len-1)])[0])
        seed_text_tok.append(out)
    print(yellow(tokenizer.detokenize(seed_text_tok)))
