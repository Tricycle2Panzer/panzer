from pyhanlp import *
import re

def get_keyword(text):
    summary_rate = 0.05
    text = re.sub(r"\n+", '\n', text)
    text = re.sub(r"\s+", '\s', text)
    text = text.replace(" ","，")
    text = text.replace("\n","。")
    l = len(HanLP.segment(text))
    k = int(l * summary_rate)
    if k < 1 :
        k = 1
    keywords = HanLP.extractKeyword(text, k)
    return keywords