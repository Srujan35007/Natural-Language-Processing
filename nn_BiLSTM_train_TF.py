import os 
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '3'
import tensorflow as tf
from tensorflow.keras import models, layers, optimizers
import numpy as np 
from tokenizer import Tokenizer
from curtsies.fmtfuncs import bold, red, blue, yellow, cyan
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

def get_all_pad_sequences(sequence, min_len=2, max_len=20, pad_type='pre'):
    all_seq = []
    len_sequence = len(sequence)
    for i in range(len_sequence-min_len+1):
        if pad_type == 'pre':
            all_seq.append([0]*(i+max_len-len_sequence) + sequence[:len_sequence-i])
        elif pad_type == 'post':
            all_seq.append(sequence[:len_sequence-i]+[0]*(i+max_len-len_sequence))
        else:
            print(f"only 'pre' or 'post' padding allowed.")
            exit()
    return all_seq

def make_one_hot(index, total_dims):
    vec = [0]*total_dims
    vec[index] = 1
    return vec

list_of_sentences = []
raw_data_path = './Datasets/cleaned_Comments_and_Replies_Reddit_funny.txt'
with open(raw_data_path, 'r') as read_file:
    for line in read_file.readlines():
        list_of_sentences.append(line.replace('\n',''))

# Tokenizing
tokenizer = Tokenizer(list_of_sentences, 1000)
total_words = len(tokenizer.word_index)+1
max_seq_len = tokenizer.max_sequence_len

# Preprocessing data
input_sequences = []
for sentence in tokenizer.list_of_sentences:
    tok_sentence = tokenizer.tokenize(sentence)
    input_sequences = input_sequences + get_all_pad_sequences(tok_sentence)
X_train, labels = np.asarray(input_sequences)[:, :-1], np.asarray(input_sequences)[:, -1]
y_train = np.asarray([make_one_hot(label, total_words) for label in labels])
print(f"Number of input sequences = {len(input_sequences)}")
print(f"X_train shape = {X_train.shape}")
print(f"y_train shape = {y_train.shape}")


# The Bidirectional LSTM model
print('\n')
optim = optimizers.Adam(learning_rate=0.01)
model = models.Sequential()
model.add(layers.Embedding(total_words,75,input_length=max_seq_len-1))
model.add(layers.Bidirectional(layers.LSTM(150)))
model.add(layers.Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=optim, metrics=['accuracy'])
print(model.summary())

model.fit(X_train, y_train, epochs=13)

print('\nTest you model:')
print(f"{red('save()')} to save the model")
print(f"{red('quit()')} to quit\n\n")
while True:
    MAX_WORDS = 20
    seed_text = input(bold(cyan(">> "))).lower().strip()
    if seed_text == 'save()':
        from datetime import datetime
        now_ = datetime.now().strftime("%d_%b_%Y_%H_%M_%S")
        model.save(f"./BiLSTM_{now_}")
        tokenizer.save()
        exit()
    elif seed_text == 'quit()':
        exit()
    else:
        pass
    seed_text_tok = tokenizer.tokenize(seed_text)
    len_seed_text = len(seed_text_tok)
    for _ in range(MAX_WORDS-len_seed_text):
        out = np.argmax(model.predict([pad_sequence(seed_text_tok, max_len=max_seq_len-1)])[0])
        seed_text_tok.append(out)
    print(yellow(tokenizer.detokenize(seed_text_tok)))
