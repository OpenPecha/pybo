# coding: utf-8
from collections import defaultdict
from pathlib import Path


def reorder_data(data):
    ordered = []
    for entry, e in data.items():
        count = 0
        for _, files in e.items():
            count += len(files)
        ordered.append((count, {entry: e}))
    ordered = sorted(ordered, reverse=True, key=lambda x: x[0])
    return ordered


def profile_report(pathname):
    pathname = Path(pathname)
    data = {}

    for d in sorted(pathname.glob("*")):
        # filter unwanted directories and files
        dirs_ignored = ["adjustment", "entry_data"]
        if not d.is_dir() or d.name in dirs_ignored or d.name.startswith("."):
            continue

        for f in sorted(d.glob("*.tsv")):
            lines = f.read_text(encoding="utf-8-sig").splitlines()
            for num, line in enumerate(lines):
                if line.startswith("#"):
                    continue
                entry = line.split("\t", 1)[0]
                path = f"{d.name}/{f.name}"

                if entry not in data:
                    data[entry] = {}
                if line not in data[entry]:
                    data[entry][line] = []

                data[entry][line].append((path, num))

    data = reorder_data(data)

    # filter and format all entries that have similar forms over files
    report = ["WORD\tENTRY\tFILE-NAME\tLINE-NUMBER"]
    count = defaultdict(int)
    for num, d in data:
        count[num] += 1
        for entry, e in d.items():
            tmp = []
            tmp.append(f"{entry}: {num}")
            for line, files in e.items():
                tmp.append(f'\t"{line}"')
                tmp.extend([f"\t\t{f}\t{n}" for f, n in files])
            report.extend(tmp)
    report = (
        [f"total distinct entries: {len(data)}"]
        + [f"entries with {a} entries: {b}" for a, b in count.items()]
        + [""]
        + report
    )
    report = "\n".join(report)

    # print to file
    out = pathname / (pathname.name + "_report.tsv")
    out.write_text(report, encoding="utf-8-sig")
