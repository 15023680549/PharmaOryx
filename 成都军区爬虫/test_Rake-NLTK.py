#!/usr/bin/Python
# -*- coding: utf-8 -*
from rake_nltk import Rake
import nltk
# print(nltk.find("."))
# from nltk.book import *

#
# print("hello")
#
r = Rake()
my_test = 'My father was a self-taught mandolin player. He was one of the best string instrument players in our town. He could not read music, but if he heard a tune a few times, he could play it. When he was younger, he was a member of a small country music band. They would play at local dances and on a few occasions would play for the local radio station. He often told us how he had auditioned and earned a position in a band that featured Patsy Cline as their lead singer. He told the family that after he was hired he never went back. Dad was a very religious man. He stated that there was a lot of drinking and cursing the day of his audition and he did not want to be around that type of environment.'

## Rake
# rake_nltk_var = Rake(max_length=2)
# rake_nltk_var.extract_keywords_from_text(my_test)
# keyword_extracted = rake_nltk_var.get_ranked_phrases()


# 要提取关键词的文本
r.extract_keywords_from_text(my_test)
# 获取关键词
print(r.get_ranked_phrases())
print("==============================")
print(r.get_ranked_phrases_with_scores())
print("===========================")
print(r.stopwords)
print("=============================")
print(r.get_word_degrees())
