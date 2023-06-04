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
retail = pd.read_excel(path + '/input/retail & wholesale.xlsx')
retail = retail[(retail['Global_Company_Size'] != 'Unknown')]  # 4867-->2279 companies

location_name = ['Texas', 'Florida', 'New Jersey', 'California', 'New York State']

retail_pure = retail[
    ['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries', 'Jobs', 'Industry']].drop_duplicates(
    ['name'])  # no location

locat = retail[['name', 'location']].groupby(['name'])
location_all = []
for item in retail_pure['name']:
    str = ''
    index = list(locat.groups[item])
    for item1 in index:
        str += retail.loc[item1, 'location']
        str += ','
    location_all.append(str)
retail_pure['location'] = location_all

for item in location_name:
    name = item + '_color'
    retail_pure[name] = [x.find(item) for x in list(retail_pure['location'])]

retail_pure = retail_pure.reset_index(drop=True)
print(retail_pure)

red = []
for i in range(len(retail_pure['name'])):
    if retail_pure.loc[i, 'Florida_color'] != -1 or retail_pure.loc[i, 'Texas_color'] != -1:
        red.append(1)
    else:
        red.append(0)

blue = []
for i in range(len(retail_pure['name'])):
    if retail_pure.loc[i, 'New Jersey_color'] != -1 or retail_pure.loc[i, 'California_color'] != -1 or \
            retail_pure.loc[i, 'New York State_color'] != -1:
        blue.append(1)
    else:
        blue.append(0)
retail_pure['blue'] = blue
retail_pure['red'] = red

color = []
for i in range(len(retail_pure['name'])):
    if retail_pure.loc[i, 'blue'] == 1 and retail_pure.loc[i, 'red'] == 1:
        color.append('red&blue')
    elif retail_pure.loc[i, 'blue'] == 1 and retail_pure.loc[i, 'red'] == 0:
        color.append('blue')
    elif retail_pure.loc[i, 'blue'] == 0 and retail_pure.loc[i, 'red'] == 1:
        color.append('red')

retail_pure['color'] = color

columns = ['Reviews', 'Salaries', 'Jobs']
for column in columns:
    name = 'num_' + column
    new_column = []
    for item in retail_pure[column]:
        item1 = item.split('K')
        if len(item1) == 1:
            if item1[0] == '--':
                new_column.append(0)
            else:
                new_column.append(float(item1[0]))
        else:
            new_column.append(int(float(item1[0]) * 1000))
    retail_pure[name] = new_column
retail_pure.to_excel(path + '/output/retail_pure_new.xlsx', index=False)

retail_pure_1 = retail_pure[['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries',
                             'Jobs', 'Industry', 'location', 'num_Reviews', 'num_Salaries', 'num_Jobs']]
print(retail_pure_1.describe().to_latex())
# print(retail_pure.describe().to_latex())


train_dataset = retail_pure[
    ['name', 'overall_rating', 'Global_Company_Size', 'num_Reviews', 'num_Salaries', 'num_Jobs', 'Industry', 'location',
     'color']]

print(train_dataset)

train, test = train_test_split(train_dataset, test_size=0.1, random_state=0)

# subsample_size = 4000  # subsample subset of data for faster demo, try setting this to much larger values
# train_data = train_dataset1.sample(n=subsample_size, random_state=0)

# overall_rating
save_path = 'agModels-predictClass_rating_retail_new'  # specifies folder to store trained models
predictor = TabularPredictor(label='overall_rating', path=save_path, eval_metric='r2').fit(train)
print(predictor.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_jobs
train2, test2 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_job_retail_new'  # specifies folder to store trained models
predictor2 = TabularPredictor(label='num_Jobs', path=save_path, eval_metric='r2').fit(train2)
print(predictor2.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_reviews
train3, test3 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_review_retail_new'  # specifies folder to store trained models
predictor3 = TabularPredictor(label='num_Reviews', path=save_path, eval_metric='r2').fit(train3)
print(predictor3.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')

# num_salaries
train4, test4 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_salary_retail_new'  # specifies folder to store trained models
predictor4 = TabularPredictor(label='num_Salaries', path=save_path, eval_metric='r2').fit(train4)
print(predictor4.feature_importance(train).to_latex())
print(
    '________________________________________________________________________________________________________________')
