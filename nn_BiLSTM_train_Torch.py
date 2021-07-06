import time 
import torch 
import torch.nn as nn 
import torch.nn.functional as F 
import torch.optim as optim 
import numpy as np 
from tokenizer import Tokenizer
import matplotlib.pyplot as plt 
from torchvision import transforms 
from torch.utils.data import DataLoader
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
train_data = [[torch.tensor(x),torch.tensor(y)] for x,y in zip(X_train, y_train)]
composed_transforms = transforms.Compose([transforms.ToTensor()])
train_loader = DataLoader(train_data, shuffle=True, batch_size = 32)
del(X_train)
del(y_train)
del(labels)
del(input_sequences)
print(f"Preprocessing complete")


