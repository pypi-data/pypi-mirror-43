from pathlib import Path
from itertools import count


class Counter():

    def __init__(self, start=0):
        self.count = start
        self.start = start

    def reset(self):
        self.count = self.start

    def next(self):
        self.count += 1
        return self.count


def fetch_file_argument():
    import sys
    args = sys.argv[1:]
    if len(args) == 1:
        pth = Path(args[0])
        if pth.exists():
            return pth
        raise Exception(f'Provided path does not exist! {pth}')
