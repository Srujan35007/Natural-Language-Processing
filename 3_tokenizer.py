class Tokenizer():
    def __init__(self, list_of_sentences=None, num_sentences=None, load_path=None):
        import time 
        import random 
        start_time = time.time()
        if list_of_sentences is not None and load_path is None:
            if num_sentences is not None and type(num_sentences) == int:
                random.shuffle(list_of_sentences)
                self.list_of_sentences = list_of_sentences[:num_sentences]
            elif num_sentences == None:
                self.list_of_sentences = list_of_sentences
            else:
                pass
            print(f"Number of sentences = {len(self.list_of_sentences)}")
            self.tuples_words_ranks = self._make_sorted_words(self.list_of_sentences)
            self._sorted_words = [elem[0] for elem in self.tuples_words_ranks]
            self._sorted_ranks = [elem[1] for elem in self.tuples_words_ranks]
            end_time = time.time()
            print(f"Tokenizing complete in {(end_time-start_time):.2f} seconds.")

        elif list_of_sentences == None and load_path is not None:
            self.list_of_sentences, self.tuples_words_ranks = self.load(load_path)
            self._sorted_words = [elem[0] for elem in self.tuples_words_ranks]
            self._sorted_ranks = [elem[1] for elem in self.tuples_words_ranks]
            print(f"Corpus with {len(self.list_of_sentences)} sentences loaded.")
            print(f"Number of unique words = {len(self.tuples_words_ranks)}.")

        else:
            print("WARNING: Tokenizer [init] Enter valid arguments")


    def _make_sorted_words(self, sub_corpus):
        line_sub_corpus = ' '.join(sub_corpus)
        bag_of_words = [word for word in line_sub_corpus.split(' ')]
        unique_words = list(set(bag_of_words))
        print(f"Number of words = {len(bag_of_words)}")
        print(f"Number of unique words = {len(unique_words)}")
        
        # get ranks of unique words
        sort_func = lambda x : x[-1]
        tuples_words_counts = []
        final_words_ranks = []
        for word in unique_words:
            tuples_words_counts.append((word, bag_of_words.count(word)))
        tuples_words_counts.sort(reverse=True, key=sort_func)
        rank = 1
        for element in tuples_words_counts:
            final_words_ranks.append((element[0],rank))
            rank += 1
        return final_words_ranks     
    
    def __repr__(self):
        return f"<Tokenizer Object>\nUnique Words = {len(self.tuples_words_ranks)}\n"+\
        f"Number of sentences = {len(self.list_of_sentences)}"

    def tokenize(self, sentence, delimiter=' '):
        result = []
        for word in sentence.split(delimiter):
            if word.lower() in self._sorted_words:
                result.append(self._sorted_ranks[self._sorted_words.index(word.lower())])
            else:
                result.append(0)
        return result
    
    def save(self, save_file_path=None):
        import pickle
        if save_file_path is None:
            from datetime import datetime
            _now = datetime.now().strftime("%d_%b_%Y_%H_%M_%S")
            _save_path = f'./tokenizer_savefile_{_now}.pickle'
        else:
            if save_file_path.endswith('.pickle'):
                _save_path = save_file_path
            else:
                print(f"WARNING: [saving] Must be a .pickle file.")
                exit()
        with open(_save_path, 'wb') as save_file:
            pickle.dump([self.list_of_sentences, self.tuples_words_ranks], save_file)
        print(f"Saved to {_save_path}")

    def load(self, load_file_path):
        import pickle
        if load_file_path.endswith('.pickle'):
            with open(load_file_path, 'rb') as load_file:
                return pickle.load(load_file)
        else:
            print(f"WARNING: [loading] Must be a .pickle file.")
            exit()
