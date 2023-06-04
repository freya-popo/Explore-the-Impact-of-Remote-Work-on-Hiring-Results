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
financial = pd.read_excel(path + '/input/financial services.xlsx')
financial = financial[(financial['Global_Company_Size'] != 'Unknown')]  # 2440 companies

#red = ['Texas', 'Florida']
# blue = ['New Jersey', 'California', 'New York State']
location_name = ['Texas', 'Florida', 'New Jersey', 'California', 'New York State']

financial_pure = financial[
    ['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries', 'Jobs', 'Industry']].drop_duplicates(
    ['name'])  # no location

# financial_pure = financial1.drop_duplicates(['name'])   # keep one line for each campany

locat = financial[['name', 'location']].groupby(['name'])
location_all = []
for item in financial_pure['name']:
    str = ''
    index = list(locat.groups[item])
    for item1 in index:
        str += financial.loc[item1, 'location']
        str += ','
    location_all.append(str)
financial_pure['location'] = location_all

for item in location_name:
    name = item + '_color'
    financial_pure[name] = [x.find(item) for x in list(financial_pure['location'])]

financial_pure = financial_pure.reset_index(drop=True)


red = []
for i in range(len(financial_pure['name'])):
    if financial_pure.loc[i, 'Florida_color'] != -1 or financial_pure.loc[i, 'Texas_color'] != -1:
        red.append(1)
    else:
        red.append(0)

blue = []
for i in range(len(financial_pure['name'])):
    if financial_pure.loc[i, 'New Jersey_color'] != -1 or financial_pure.loc[i, 'California_color'] != -1 or \
            financial_pure.loc[i, 'New York State_color'] != -1:
        blue.append(1)
    else:
        blue.append(0)
financial_pure['blue'] = blue
financial_pure['red'] = red

color = []
for i in range(len(financial_pure['name'])):
    if financial_pure.loc[i, 'blue'] == 1 and financial_pure.loc[i, 'red'] == 1:
        color.append('red&blue')
    elif financial_pure.loc[i, 'blue'] == 1 and financial_pure.loc[i, 'red'] == 0:
        color.append('blue')
    elif financial_pure.loc[i, 'blue'] == 0 and financial_pure.loc[i, 'red'] == 1:
        color.append('red')

financial_pure['color'] = color
financial_pure.to_excel(path + '/output/financial_pure_new.xlsx', index=False)

columns = ['Reviews', 'Salaries', 'Jobs']
for column in columns:
    name = 'num_' + column
    new_column = []
    for item in financial_pure[column]:
        item1 = item.split('K')
        if len(item1) == 1:
            if item1[0] == '--':
                new_column.append(0)
            else:
                new_column.append(float(item1[0]))
        else:
            new_column.append(int(float(item1[0]) * 1000))
    financial_pure[name] = new_column

financial_pure_1 = financial_pure[['name', 'overall_rating', 'Global_Company_Size', 'Reviews', 'Salaries',
                                   'Jobs', 'Industry', 'location', 'num_Reviews', 'num_Salaries', 'num_Jobs']]
print(financial_pure_1.describe().to_latex())

financial_pure.to_excel(path + '/output/financial_pure_new.xlsx', index=False)
train_dataset = financial_pure[
    ['name', 'overall_rating', 'Global_Company_Size', 'num_Reviews', 'num_Salaries', 'num_Jobs', 'Industry', 'location',
     'color']]

print(train_dataset)


# subsample_size = 4000  # subsample subset of data for faster demo, try setting this to much larger values
# train_data = train_dataset1.sample(n=subsample_size, random_state=0)

# overall_rating
train, test = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_rating_financial_new'  # specifies folder to store trained models
predictor = TabularPredictor(label='overall_rating', path=save_path, eval_metric='r2').fit(train)
print(predictor.feature_importance(train).to_latex())
feature_importance = predictor.feature_importance(train).iloc[:, [0, 1]]

# num_jobs
train2, test2 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_job_financial_new'  # specifies folder to store trained models
predictor2 = TabularPredictor(label='num_Jobs', path=save_path, eval_metric='r2').fit(train2)
print(predictor2.feature_importance(train2).to_latex())


# num_reviews
train3, test3 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_review_financial_new'  # specifies folder to store trained models
predictor3 = TabularPredictor(label='num_Reviews', path=save_path, eval_metric='r2').fit(train3)
print(predictor3.feature_importance(train3).to_latex())


# num_salaries
train4, test4 = train_test_split(train_dataset, test_size=0.1, random_state=0)
save_path = 'agModels-predictClass_salary_financial_new'  # specifies folder to store trained models
predictor4 = TabularPredictor(label='num_Salaries', path=save_path, eval_metric='r2').fit(train4)
print(predictor4.feature_importance(train4).to_latex())




