<h1 align="center">
  <br>
  <a href="https://buddhistai.tools/"><img src="https://raw.githubusercontent.com/WeBuddhist/visual-assets/refs/heads/main/logo/WB-logo-purple.png" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<h1 align="center">pybo</h1>

<p align="center">
  |Python| |MIT|
</p>

🦜 NLP for Tibetan, in Python.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#contributing)
- [How to get help](#how-to-get-help)
- [Terms of use](#terms-of-use)

## Features

- Tibetan Natural Language Processing
- Word segmentation
- Tokenization
- Part-of-speech tagging
- Integration with Botok

## Prerequisites

- Python 3.8+

## Installation

```bash
pip install pybo
```

Or from source:

```bash
git clone https://github.com/OpenPecha/pybo.git
cd pybo
pip install -e .
```

## Usage

```python
import pybo

# Example usage
text = "བོད་ཡིག"
result = pybo.segment(text)
print(result)
```

## How to get help
* File an issue.
* Join our [discord](https://discord.com/invite/7GFpPFSTeA).

## Terms of use
pybo is licensed under the [MIT License](/LICENSE).