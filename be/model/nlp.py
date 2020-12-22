from pyhanlp import *
import jieba
import re

def get_keyword(text):
    summary_rate = 0.015
    text = re.sub(r"\n+", '\n', text)
    text = re.sub(r"\s+", ' ', text)
    text = text.replace(" ","，")
    text = text.replace("\n","。")
    l = len(HanLP.segment(text))
    k = int(l * summary_rate)
    if k < 1 :
        k = 1
    keywords = HanLP.extractKeyword(text, k)
    return keywords

def get_preffix(text):
    l = len(text)
    pre = []
    for i in range(1,l+1):
        pre.append(text[:i])
    return pre

def get_middle_ffix(text):
    word_list = list(jieba.cut(text))
    l = len(word_list)
    middle = []
    words = ""
    for i in range(l):
        words = word_list[l-i-1] + words
        middle += get_preffix(words)
    middle = list(set(middle))
    return middle

def get_country(text):
    pattern = r'\[[^()]\]'
    #pattern = r'\[[^()]*\]'
    country = re.search(pattern,text)
    if not country:
        print('author region is NULL')
        return '[中]'
    else:
        auth_country = list(country.group())
        print('author region:' + country.group())
    return country.group()
