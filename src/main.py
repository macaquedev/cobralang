from typing import List
import os
import colorama
import difflib
from .executor import CobralangExecutor


def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def get_similar_files(filename: str) -> List[str]:
    dirname = os.path.dirname(os.path.abspath(filename))

    try:
        paths = [os.path.join(dirname, i) for i in os.listdir(dirname) if i.endswith(".cb")]
    except FileNotFoundError as e:
        return 1

    for directory in [i for i in os.listdir(dirname) if os.path.isdir(i)]:
        paths.extend([
            os.path.join(dirname, directory, i) for i in os.listdir(os.path.abspath(directory)) if i.endswith(".cb")
        ])

    paths.sort(key=lambda x: similar(x, os.path.abspath(filename)), reverse=True)
    return paths


def repl():
    executor = CobralangExecutor()
    print("Cobralang Version 0.1.0")
    print("Created by macaquedev\n")
    while True:
        code = input("cobra >>> ")
        executor.execute("<repl>", code, [])


def exec_file(filename: str, args: List[str]):
    try:
        with open(filename) as f:
            code = f.read()
            executor = CobralangExecutor()
            executor.execute(filename, code, args)

    except FileNotFoundError:
        print(f"cobralang > {colorama.Fore.RED}ERROR: {colorama.Style.RESET_ALL}"
              f"Can't open file \"{os.path.abspath(filename)}\", no such file found.")
        files = get_similar_files(filename)
        if files == 1:
            print(f"No such directory found: '{os.path.abspath(filename)}'")
            return
        if len(files) > 5:
            files = files[:5]
            print("Showing only top 5 results as more than 5 .cb files found.")
        elif len(files) == 0:
            print("No .cb files found in directory. Have you given your file the correct file extension?")
            return
        print("Did you mean: ")
        length = max([len(i) for i in files]) + 5
        for file in files:
            print(f"    {colorama.Fore.YELLOW}cobralang{colorama.Style.RESET_ALL} {file.ljust(length)} "
                  f"{colorama.Fore.GREEN}Similarity: {colorama.Style.RESET_ALL}"
                  f"{round(similar(os.path.abspath(filename), file) * 100, 2)}%")
