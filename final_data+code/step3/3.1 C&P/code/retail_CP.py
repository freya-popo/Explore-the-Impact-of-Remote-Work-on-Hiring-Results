import pandas as pd
import string
import collections
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn import preprocessing
import numpy as np
from functools import reduce
from autogluon.tabular import TabularDataset, TabularPredictor

meaningless = ['the', 'to', 'and', 'you', 'a', 'of', 'your', 'for', 'in', 'is', 'that', 'are', 'more', 'be', 'doing',
               'have', 'on', 'what', 'it', 'with', 'they', 'not', 'i', 'all', 'so', 'as', 'them', 'do', 'us', 'from',
               'at', 'can', 'this', 'or', 'about', 'we', 'how', 'just', 'an', 'dont', 'if', 'than', 'but', 'when',
               'being', 'by', 'who', 'its', 'some', 'my', 'much', 'only', 'our', 'other', 'me', 'also', 'here', 'has',
               'any', 'will', 'then', 'was', 'could', 'too', 'there', ' ', '•', 'were', '', '--', 'which', 'where']

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code/step3/3.1 C&P'
retail_CP = pd.read_excel(path + '/input/step3CP_retail.xlsx')
good = []
num_good = []
bad = []
num_bad = []
for item in retail_CP['pros']:
    print(item)

    if pd.isna(item) != True:
        lst = item.split('\xa0')
        print(lst, lst[1].split(' ')[1])
        # good.append(lst[0].strip().strip('"'))
        ppp = lst[0]
        for i in string.punctuation:
            ppp = ppp.replace(i, '')
        good.append(ppp)
        if len(lst) > 1:
            num_good.append(int(lst[1].split(' ')[1]))
        else:
            num_good.append(0)
    else:
        good.append('')
        num_good.append(0)

for item in retail_CP['cons']:
    print(item)
    if pd.isna(item) != True:
        lst = item.split('\xa0')
        # bad.append(lst[0].strip().strip('"'))
        ccc = lst[0]
        for i in string.punctuation:
            ccc = ccc.replace(i, '')
        bad.append(ccc)
        if len(lst) > 1:
            num_bad.append(int(lst[1].split(' ')[1]))
        else:
            num_bad.append(0)
    else:
        bad.append('--')
        num_bad.append(0)

retail_CP['good'] = good
retail_CP['num_good'] = num_good
retail_CP['bad'] = bad
retail_CP['num_bad'] = num_bad
print(retail_CP)
retail_CP.to_excel(path + '/output/retail_CP_processed.xlsx', index=False)

# print(retail_CP.describe().to_latex())

# 词频统计
frequency_retail = pd.DataFrame()
str_pros = ''
for item in retail_CP['good']:
    str_pros += item.lower() + ' '
# print(str_pros)
lst_new_pros = []
for item in str_pros.split(' '):
    item1 = item.strip()
    if item1 not in meaningless:
        lst_new_pros.append(item1)
        print(item1, 'yesssss')
    else:
        print(item1)
dic_pros = dict(collections.Counter(lst_new_pros))
frequency_retail_pros = pd.DataFrame(list(dic_pros.items()))
frequency_retail_pros.to_excel(path + '/output/retail_CP_frequency_pros.xlsx', index=False)
print(dic_pros.keys())
str_cons = ''
for item in retail_CP['bad']:
    str_cons += item.lower() + ' '
# print(str_pros)
lst_new_cons = []
for item in str_cons.split(' '):
    item1 = item.strip()
    if item1 not in meaningless:
        lst_new_cons.append(item1)
dic_cons = dict(collections.Counter(lst_new_cons))
print(dic_cons.keys())
frequency_retail_cons = pd.DataFrame(list(dic_cons.items()))
frequency_retail_cons.to_excel(path + '/output/retail_CP_frequency_cons.xlsx', index=False)
