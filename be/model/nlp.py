from pyhanlp import *
import jieba
import re

def get_keyword(text):
    if isinstance(text,str) == False:
        return []
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
    if isinstance(text,str) == False:
        return []
    l = len(text)
    pre = []
    for i in range(1,l+1):
        pre.append(text[:i])
    return pre

def get_middle_ffix(text):
    if isinstance(text,str) == False:
        return []
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
    if isinstance(text,str) == False:
        return ""
    pattern_brace = r'\([^()]\)'
    pattern = r'\[[^()]\]'
#     pattern = r'\[[^()]*\]'
    country = re.search(pattern,text)
    country_brace = re.search(pattern_brace,text)
    if not country and not country_brace:
        print('author region is NULL')
        return '中'
    elif country_brace:
        auth_country = list(country_brace.group())
        print('author region:' + country_brace.group())
        return country_brace.group()[1]
    else:
        auth_country = list(country.group())
        print('author region:' + country.group())
        return country.group()[1]

def get_country_and_author(text):
    if isinstance(text,str) == False:
        return "", ""
    l = len(text)
    b = False
    country = ""
    author = ""
    for i in range(l):
        if text[i] in ")]}）】」":
            b = False
        elif b == True:
            country += text[i]
        elif text[i] in "([{（【「":
            b = True
            if country != "":
                country += "_"
        else:
            author += text[i]
            continue
    return country, author

def parse_name(text):
    if isinstance(text,str) == False:
        return []
    pre = 0
    l = len(text)
    names = []
    for i in range(l):
        if text[i] in '・· ,， ':
            if text[pre:i] != "":
                names.append(text[pre:i])
            pre = i+1
    names.append(text[pre:l])
    return names