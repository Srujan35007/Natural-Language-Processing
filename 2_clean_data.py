import time 
from argparse import ArgumentParser as AP 
from tqdm import tqdm #pip install tqdm 
from curtsies.fmtfuncs import red, yellow, cyan, bold #pip install curtsies
print(f"Imports complete.")

def clean_comment(raw_line, min_len=7, max_len=20, delimiter='<::>', new_line_token="<NEWLINE>"):
    num_exceptions = 0
    stop_patterns = [
            'https://',
            'http://',
            'www.',
            '[deleted]',
            '[removed]',
            'u/',
            'r/'
            ]
    clean_sentences = []
    try:
        raw_comment = raw_line.split(delimiter)[3]
        new_line_split = raw_comment.lower().split(new_line_token)
        for newline in new_line_split:
            full_stop_split = newline.split('.')
            for sentence in full_stop_split:
                clean_words = []
                num_clean_words = 0
                for word in sentence.split(' '):
                    has_stop_pattern = False
                    for stop_pattern in stop_patterns:
                        if stop_pattern in word:
                            has_stop_pattern = True
                        else:
                            pass
                    if has_stop_pattern:
                        pass
                    else:
                        if word.isalpha():
                            clean_words.append(word)
                            num_clean_words += 1
                if min_len <= num_clean_words <= max_len:
                    clean_sentences.append(' '.join(clean_words))
                else:
                    pass
    except:
        num_exceptions += 1
    return [comment for comment in clean_sentences if comment != ''] 

if __name__ == '__main__':
    parser = AP()
    parser.add_argument('raw_file_path')
    args = parser.parse_args()

    orig_file_path = args.raw_file_path.split('/')[-1]
    n_comments = 0
    cleaned_file_path = f'./cleaned_{orig_file_path}'
    with open(args.raw_file_path, 'r') as read_file:
        with open(cleaned_file_path, 'w') as write_file:
            for line in tqdm(read_file.readlines()):
                sentences_ = clean_comment(line)
                if len(sentences_) > 0:
                    for sentence_ in sentences_:
                        write_file.write(str(sentence_.replace('\n',''))+'\n')
                        n_comments += 1
                else:
                    pass
    print(bold(cyan(f"Clean comments = {n_comments}")))
