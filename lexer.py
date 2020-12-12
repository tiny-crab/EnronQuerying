import os
import json


def flat_map(xs): return [y for ys in xs for y in ys]


def splitter(search_dir, out_dir):
    tokens = {}

    for dirpath, dirnames, files in os.walk(search_dir):
        print(f'Working on directory: {dirpath}')
        for filename in files:
            name = os.path.join(dirpath, filename)
            with open(name, 'r') as file:
                # TODO optimize list -> set -> list conversion
                # TODO due to keys being based on filepath, this could potentially lead to message ID duplication
                tokens[name] = list(set(file.read().split()))

        if tokens:
            # TODO improve -2 access? it's magic
            output_dir = os.path.join(out_dir, os.path.split(dirpath)[-2])
            print(f'Outputting to directory: {output_dir}')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, "tokens.txt")
            with open(output_file, 'w') as out:
                json.dump(tokens, out)
                tokens.clear()
