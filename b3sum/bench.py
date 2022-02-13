#! /usr/bin/env python3

import os
from os import path
import subprocess
import sys
import time

HERE = path.dirname(__file__)
NUM_RUNS = 5


def one_run():
    if os.environ.get("FLUSH") == "1":
        subprocess.run(
            ["sudo", "tee", "/proc/sys/vm/drop_caches"],
            input=b"3\n",
            stdout=subprocess.DEVNULL,
            check=True,
        )
    start = time.monotonic()
    subprocess.run(
        [path.join(HERE, "target/release/b3sum")] + sys.argv[1:],
        stdout=subprocess.DEVNULL,
        check=True,
    )
    end = time.monotonic()
    print(".", end="")
    sys.stdout.flush()
    assert end > start
    return end - start


def median_run():
    assert NUM_RUNS % 2 == 1, "NUM_RUNS should be odd"
    times = []
    for _ in range(NUM_RUNS):
        t = one_run()
        times.append(t)
    times.sort()
    return times[len(times) // 2]


def main():
    subprocess.run(
        ["cargo", "build", "--release"],
        check=True,
        cwd=HERE,
    )
    t = median_run()
    print()
    print("{:.3f}".format(t))


if __name__ == "__main__":
    main()
