import numpy as np
import pandas as pd
import string
import collections
import math

meaningless = ['the', 'to', 'and', 'you', 'a', 'of', 'your', 'for', 'in', 'is', 'that', 'are', 'more', 'be', 'doing',
               'have', 'on', 'what', 'it', 'with', 'they', 'not', 'i', 'all', 'so', 'as', 'them', 'do', 'us', 'from',
               'at', 'can', 'this', 'or', 'about', 'we', 'how', 'just', 'an', 'dont', 'if', 'than', 'but', 'when',
               'being', 'by', 'who', 'its', 'some', 'my', 'much', 'only', 'our', 'other', 'me', 'also', 'here', 'has',
               'any', 'will', 'then', 'was', 'could', 'too', 'there', ' ', '•', 'were', '', '--', 'which', 'where']

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code'


def readin(industry):
    data = pd.read_excel(path + '/step3/input/step3reviews_' + industry + '.xlsx')
    data['Year'] = [x.split(', ')[1] for x in data['time']]
    data['Month'] = [x.split(' ')[0] for x in data['time']]
    return data


def process(data):
    help = []
    for item in data['helpful']:
        if item.find('first') != -1:
            help.append(0)
        else:
            help.append(int(item[0]))
    data['help'] = help

    status1 = []
    status2 = []
    status3 = []

    for item in data['status_']:
        item1 = item.split(', ')
        if item1[0].find('Former') != -1:
            status1.append(0)
        else:
            status1.append(1)
        if len(item1) > 1:
            # if item1[1].find('than') != -1:
            item2 = item1[1].split('than ')
            status2.append(int(item2[1][0]))
            status3.append(int(item2[1][0]))
        else:
            status2.append(np.nan)

    data['status1'] = status1
    data['status2'] = status2
    data['status2'].fillna(np.mean(status3), inplace=True)
    for column in ['recommend', 'CEO', 'businessOutlook']:
        lst = []
        for item in data[column]:
            if item == '红色':
                lst.append(-1)
            elif item == '绿色':
                lst.append(1)
            else:
                lst.append(0)
        data[column + '_v'] = lst

    for column in ['title', 'pros', 'cons', 'advice']:
        lst = []
        # data[column].fillna(' ')
        for item in data[column]:
            if pd.isna(item) != True:
                for i in string.punctuation:
                    item = item.replace(i, '')
                lst.append(item.replace('\n', ' '))
            else:
                lst.append('')
        data[column + '_new'] = lst

    job = []
    location = []
    for item in data['position']:
        item1 = item.split(', ')
        job.append(item1[0])
        if len(item1) > 1:
            location.append(item1[1])
        else:
            location.append(np.nan)
    data['job'] = job
    data['location'] = location
    return data


def review(data):
    review = data[['Year', 'title_new', 'pros_new', 'cons_new', 'advice_new', 'location']]
    review_need = review[review['Year'].isin(['2020', '2021', '2022'])]
    text = review_need[['location', 'pros_new', 'cons_new']]
    review_location1 = []
    review_location2 = []
    # total_loctaions_fin = pd.ExcelWriter(path + '/output/review_processed_financial_5_locations.xlsx')
    for lo in ['CA', 'NY', 'NJ', 'TX', 'FL']:
        review_lo = text[text['location'] == lo]
        if lo in ['CA', 'NY', 'NJ']:
            review_location1.append(review_lo)
        else:
            review_location2.append(review_lo)
        # print(review_lo)
        # review_lo.to_excel(total_loctaions_fin, sheet_name=lo, index=False)
    # total_loctaions_fin.save()
    group1 = pd.concat(review_location1)
    group2 = pd.concat(review_location2)
    return group1, group2


def frequency(data, column, industry, group):
    lst = data[column]
    s = ''
    for item in lst:
        s += item.lower() + ' '
    lst_new = []
    for item in s.split(' '):
        if item not in meaningless:
            lst_new.append(item)
    # print(str_pros)
    dic = dict(collections.Counter(lst_new))
    result = pd.DataFrame(list(dic.items())).rename(columns={0: 'word', 1: 'frequency'}).sort_values(by='frequency',
                                                                                                     ascending=False)
    result.to_excel(path + '/step3/output/frequency_' + industry + '_' + column + '_' + group + '.xlsx', index=False)
    return result


for industry in ['financial', 'retail', 'technology']:
    data = readin(industry)
    processed_data = process(data)
    review_in = review(processed_data)
    for item in ['pros_new', 'cons_new']:
        result1 = frequency(review_in[0], item, industry, 'group1')
        result2 = frequency(review_in[1], item, industry, 'group2')
        print(result1)
        print(result2)
# result2 = frequency(review_f[0], 'pros_new', 'financial')
