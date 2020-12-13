import lexer
import trie
import json
import os


def preprocess():
    data_root_dir = "./sample_data/"
    split_out_dir = "./split_tokens/"
    trie_out_dir = "./trie_out"

    lexer.splitter(data_root_dir, split_out_dir)

    trie_root = trie.trie_create("./split_tokens/sample_data/")

    for child in trie_root.children:
        ser_trie_dir = os.path.join(trie_out_dir, child.char)
        print(f"Dumping data into {ser_trie_dir}")
        if not os.path.exists(ser_trie_dir):
            os.makedirs(ser_trie_dir)
        trie_file = os.path.join(ser_trie_dir, "trie.txt")
        with open(trie_file, 'w') as file:
            file.write(json.dumps(child.serialize()))
        print(f"Wrote trie to {trie_file}")
