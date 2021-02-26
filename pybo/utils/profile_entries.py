# coding: utf-8
from collections import defaultdict
from pathlib import Path


def profile_entries(pathname):
    pathname = Path(pathname)
    entries = defaultdict(list)

    profile_files = [Path(__file__).parent.parent / "resources/particles.tsv"]
    for d in pathname.glob("*"):
        # filter unwanted directories and files
        dirs_ignored = ["adjustment", "entry_data"]
        if not d.is_dir() or d.name in dirs_ignored or d.name.startswith("."):
            continue

        profile_files.extend(list(d.glob("*.tsv")))

    # add files
    for f in profile_files:
        lines = f.read_text(encoding="utf-8-sig").splitlines()
        for num, line in enumerate(lines):
            if line.startswith("#"):
                continue
            entry = line.split("\t", 1)[0]
            entries[entry].append(line)
    return entries
