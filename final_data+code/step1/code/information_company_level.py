import pandas as pd
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

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code/step1'
information = pd.read_excel(path + '/input/information Technology.xlsx')
information = information[(information['Global_Company_Size'] != 'Unknown')]  # 4867-->2279 companies

print(len(information['name']))
print(len(set(information['name'])))

location_name = ['Texas', 'Florida', 'New Jersey', 'California', 'New York State']

information_pure = information[
    ['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries', 'Jobs', 'Industry']].drop_duplicates(
    ['name'])  # no location

locat = information[['name', 'location']].groupby(['name'])
location_all = []
for item in information_pure['name']:
    str = ''
    index = list(locat.groups[item])
    for item1 in index:
        str += information.loc[item1, 'location']
        str += ','
    location_all.append(str)
information_pure['location'] = location_all

for item in location_name:
    name = item + '_color'
    information_pure[name] = [x.find(item) for x in list(information_pure['location'])]

information_pure = information_pure.reset_index(drop=True)
print(information_pure)

red = []
for i in range(len(information_pure['name'])):
    if information_pure.loc[i, 'Florida_color'] != -1 or information_pure.loc[i, 'Texas_color'] != -1:
        red.append(1)
    else:
        red.append(0)

blue = []
for i in range(len(information_pure['name'])):
    if information_pure.loc[i, 'New Jersey_color'] != -1 or information_pure.loc[i, 'California_color'] != -1 or \
            information_pure.loc[i, 'New York State_color'] != -1:
        blue.append(1)
    else:
        blue.append(0)
information_pure['blue'] = blue
information_pure['red'] = red

color = []
for i in range(len(information_pure['name'])):
    if information_pure.loc[i, 'blue'] == 1 and information_pure.loc[i, 'red'] == 1:
        color.append('red&blue')
    elif information_pure.loc[i, 'blue'] == 1 and information_pure.loc[i, 'red'] == 0:
        color.append('blue')
    elif information_pure.loc[i, 'blue'] == 0 and information_pure.loc[i, 'red'] == 1:
        color.append('red')

information_pure['color'] = color

columns = ['Reviews', 'Salaries', 'Jobs']
for column in columns:
    name = 'num_' + column
    new_column = []
    for item in information_pure[column]:
        item1 = item.split('K')
        if len(item1) == 1:
            if item1[0] == '--':
                new_column.append(0)
            else:
                new_column.append(float(item1[0]))
        else:
            new_column.append(int(float(item1[0]) * 1000))
    information_pure[name] = new_column

information_pure.to_excel(path + '/output/information_pure_new.xlsx', index=False)
# print(information_pure.describe().to_latex())
information_pure_1 = information_pure[['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries',
                                       'Jobs', 'Industry', 'location', 'num_Reviews', 'num_Salaries', 'num_Jobs']]
print(information_pure_1.describe().to_latex())

train_dataset = information_pure[
    ['name', 'overall_rating', 'Global_Company_Size', 'num_Reviews', 'num_Salaries', 'num_Jobs', 'Industry', 'location',
     'color']]

print(train_dataset)

# overall_rating
train, test = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_rating_information_new'  # specifies folder to store trained models
predictor = TabularPredictor(label='overall_rating', path=save_path, eval_metric='r2').fit(train)
print(predictor.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_jobs
train2, test2 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_job_information_new'  # specifies folder to store trained models
predictor2 = TabularPredictor(label='num_Jobs', path=save_path, eval_metric='r2').fit(train2)
print(predictor2.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_reviews
train3, test3 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_review_information_new'  # specifies folder to store trained models
predictor3 = TabularPredictor(label='num_Reviews', path=save_path, eval_metric='r2').fit(train3)
print(predictor3.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_salaries
train4, test4 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_salary_information_new'  # specifies folder to store trained models
predictor4 = TabularPredictor(label='num_Salaries', path=save_path, eval_metric='r2').fit(train4)
print(predictor4.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')
