import numpy as np
import pandas as pd
import pingouin as pg
import math

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code/step2/2.1 jobs'

location = ['California', 'Florida', 'New_Jersey', 'New_YorkState', 'Texas']
industries = ['financial', 'retail', 'technology']
for industry in industries:
    job = pd.read_excel(path + '/input/step2_opening_' + industry + '.xlsx')
    dff = pd.DataFrame()
    for item in location:
        lst = job[item].dropna()
        dff[item] = lst.describe().values
    job.fillna(0, inplace=True)
    print(dff.to_latex())

    df = pd.DataFrame()
    group1 = job[['California', 'New_Jersey', 'New_YorkState']]
    # group1['color'] = 'blue'
    group2 = job[['Florida', 'Texas']]
    # group2['color'] = 'red'

    df1 = group1.melt(var_name='location', value_name='jobs').dropna().sort_values(by='jobs')
    df1['color'] = 'blue'

    df2 = group2.melt(var_name='location', value_name='jobs').dropna().sort_values(by='jobs')
    df2['color'] = 'red'

    df['group1'] = df1['jobs'].describe().values
    df['group2'] = df2['jobs'].describe().values
    print(df.to_latex())

    df3 = df1[['color', 'jobs']]
    df4 = df2[['color', 'jobs']]
    df5 = pd.concat([df3, df4])
    result = pg.anova(data=df5, dv='jobs', between='color')
    print(result)
    print(result.to_latex())
    print('______________________________________________________________________')
