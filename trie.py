import os
import json


class TrieNode:

    def __init__(self, char='', children=None, hits=None):
        self.char = char  # char in word represented by node
        self.children = children if children is not None else []
        self.hits = hits if hits is not None else []  # file paths for any email that hits on this node

    def child_with_char(self, target_char):
        return next(child for child in self.children if child.char == target_char)

    def child_chars(self):
        return map(lambda node: node.char, self.children)

    def insert(self, key, hit):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                new_child = TrieNode(char=char)
                cur_node.children.append(new_child)
                cur_node = new_child
            else:
                cur_node = cur_node.child_with_char(char)

        cur_node.hits.append(hit)

    def search(self, key):
        cur_node = self
        for char in key:
            if char not in cur_node.child_chars():
                return False
        return cur_node.hits

    def to_dict(self):
        cur_node = self
        trie_dict = {}
        dict_key = cur_node.char
        traversal_stack = [cur_node]

        while traversal_stack:
            visited_all_children = True
            if not traversal_stack[-1].children:
                traversal_stack.pop()
                dict_key = dict_key[:-1]
            else:
                cur_node = traversal_stack[-1]
            for child in cur_node.children:
                potential_key = dict_key + child.char
                if potential_key not in trie_dict.keys():
                    visited_all_children = False
                    trie_dict[potential_key] = child
                    print(f"added {potential_key} to dict")
                    traversal_stack.append(child)
                    dict_key += child.char
                    break
            if visited_all_children:
                traversal_stack.pop()
                dict_key = dict_key[:-1]

        return trie_dict

    def from_dict(self):
        pass


def trie_create(tokens_dir):
    trie_root = TrieNode()

    for dirpath, dirnames, files in os.walk(tokens_dir):
        print(f'Adding directory to trie: {dirpath}')
        for filename in files:
            if filename == "tokens.txt":
                name = os.path.join(dirpath, filename)
                with open(name, 'r') as tokens_file:
                    tokens_by_email = json.loads(tokens_file.read())
                    for email, tokens in tokens_by_email.items():
                        for token in tokens:
                            trie_root.insert(token, email)

    return trie_root


def trie_encode(root):
    pass
