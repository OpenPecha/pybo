from pathlib import Path

from pybo import pyewts

converter = pyewts.pyewts()

uni = 'བཀྲ་ཤིས་བདེ་ལེགས།། །།'
wylie = 'bkra shis bde legs//_//'

new_uni = converter.toUnicode(wylie)
new_wylie = converter.toWylie(uni)

assert uni[:-5] == new_uni[:-3]  # double shads are a single char in pyewts
assert wylie == new_wylie
