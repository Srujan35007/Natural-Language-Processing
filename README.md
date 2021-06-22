# Natural-Language-Processing
Contains data scraping methods and NLP models

## 1. Text generation using Bidirecitonal-LSTM <br>
 - Data was collected from reddit comments. [data_scrape_from_reddit.py](./data_scrape_from_reddit.py)
 - The comments were cleaned using the script [data_clean_rawdata.py](./data_clean_rawdata.py)
 - My custom tokenizer [tokenizer.py](./tokenizer.py)
 - The Tensorflow model architecture and training in [nn_BiLSTM_train_TF.py](./nn_BiLSTM_train_TF.py)
 - Loading and testing the trained model in [load_trained_TF.py](./load_trained_TF.py)
