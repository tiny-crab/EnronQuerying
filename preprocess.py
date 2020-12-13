import lexer
import json
import os

def preprocess():
    data_root_dir = "./sample_data/"
    split_out_dir = "./split_tokens/"
    trie_out_dir = "./trie_out"

    lexer.splitter(data_root_dir, split_out_dir)

    for item in os.listdir(split_out_dir):
        tokens_file = os.path.join(item, "tokens.txt")
        if os.path.isfile(tokens_file):
            with open(tokens_file, 'r') as file:
                tokens = json.loads(file.read())
            print(f"found tokens for {item}")
