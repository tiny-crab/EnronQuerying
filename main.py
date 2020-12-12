import lexer
import json
import os

if __name__ == "__main__":
    data_root = "./sample_data/"
    split_out = "./split_tokens/"

    lexer.splitter(data_root, split_out)

    for item in os.listdir(split_out):
        tokens_file = os.path.join(item, "tokens.txt")
        if os.path.isfile(tokens_file):
            with open(tokens_file, 'r') as file:
                tokens = json.loads(file.read())
            print(f"found tokens for {item}")
