import numpy as np
import pandas as pd
import pingouin as pg

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code/step2/2.3 ratings from diff groups'

types = ['blue', 'red', 'red&blue']
groups = ['asian', 'blackAmerica', 'hispanicLatinx', 'middleEastern', 'white',
          'indigenous', 'pacificIslander', 'men', 'women', 'transgender',
          'heterosexual', 'LGBTQ', 'nonDisabled', 'peopleDisabilities',
          'notParent', 'parentsGuardians', 'Caregivers', 'nonVeterans',
          'veterans']
dic = {'gender': ['men', 'women', 'transgender'], 'disability': ['nonDisabled', 'peopleDisabilities'],
       'parent': ['notParent', 'parentsGuardians', 'Caregivers']}

industries = ['financial', 'retail', 'information']


def readin(industry):
    data = pd.read_excel(path + '/input/step2_ratings_' + industry + '.xlsx')
    return data


def process(data, type_color):
    data_type = data[data['color'] == type_color]
    for item1 in ['recommendFriend', 'approveCEO']:
        recommend = []
        recommend1 = []
        for item in data_type[item1]:
            # print(item)
            if pd.isna(item):
                recommend.append(np.NaN)
            else:
                recommend.append(int(item.split('%')[0]) * 0.01)
                recommend1.append(int(item.split('%')[0]) * 0.01)
        data_type[item1] = recommend
        data_type[item1].fillna(np.mean(recommend1), inplace=True)

    for group in groups:
        lst = []
        lst1 = []
        for value in data_type[group]:
            if pd.isna(value):
                lst.append(np.NaN)
            else:
                if value == '—':
                    lst.append(np.NaN)
                else:
                    lst.append(float(value))
                    lst1.append(float(value))
        data_type[group] = lst
        data_type[group].fillna(np.mean(lst1), inplace=True)
    return data_type


def anova_group(data, type):
    data1 = data[dic[type]]
    result = pg.anova(data=data1.melt(var_name='group', value_name='value'), dv='value', between='group')
    return result


def anova_type(data):
    groups1 = ['color','men', 'women', 'transgender', 'nonDisabled', 'peopleDisabilities', 'notParent',
               'parentsGuardians', 'Caregivers']
    type1 = process(data, 'blue')[groups1]
    type2 = process(data, 'red')[groups1]
    type3 = process(data, 'red&blue')[groups1]
    data2 = pd.concat([type1, type2, type3])
    for item in groups1[1:]:
        result = pg.anova(data=data2, dv=item, between='color')
        print(result.to_latex())


for industry in industries:
    data = readin(industry)
    anova_type(data)
    print('--------------------------------------------------------------------------------------------------------')
