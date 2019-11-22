# # coding: utf-8
# from icu import RuleBasedCollator
# from pathlib import Path
#
#
# rules = Path(__file__).parent / "../third_party/rules.txt"
# collator = RuleBasedCollator(
#     "[normalization on]\n[reorder Tibt]\n" + rules.read_text(encoding="utf-8")
# )
#
#
# def bo_sorted(word_list):
#     return sorted(word_list, key=collator.getSortKey)
