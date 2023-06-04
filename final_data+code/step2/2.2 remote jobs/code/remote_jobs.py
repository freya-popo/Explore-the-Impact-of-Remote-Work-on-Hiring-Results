import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

import pingouin as pg

pd.set_option('display.max_columns', None)
path = r'/Users/freyaxr/Documents/private/capstone/final_data+code/step2/2.2 remote jobs'

industries = ['financial', 'retail', 'information']

for industry in industries:
    remote = pd.read_excel(path + '/input/step2_remote_' + industry + '.xlsx')
    lst = []
    n = 0
    j = 0
    k = 0
    for i in range(len(remote['remote'])):
        if pd.isna(remote['remote'][i]):
            lst.append(0)
            if remote['color'][i] == 'red':
                n += 1
            elif remote['color'][i] == 'blue':
                j += 1
            elif remote['color'][i] == 'red&blue':
                k += 1
        else:
            lst.append(remote['remote'][i])
    remote['number_remote'] = lst

    data_type1 = remote[remote['color'] == 'blue']['number_remote']
    data_type2 = remote[remote['color'] == 'red']['number_remote']
    data_type3 = remote[remote['color'] == 'red&blue']['number_remote']

    plt.figure(figsize=(5, 3), dpi=120, facecolor="white", edgecolor="red")  # 建立画布
    # plt.rcParams['font.family'] = 'SimSun'
    plt.boxplot([data_type1, data_type2, data_type3], labels=["type1", "type2", "type3"])
    plt.savefig(path+'/output-boxplot/'+industry+".jpg", dpi=300, bbox_inches="tight")
    plt.title('number of remote jobs in ' + industry + ' industry')
    plt.show()  # 展示箱线图

    data = {'group1': data_type1, 'group2': data_type2, 'group3': data_type3}
    df = pd.DataFrame(data)
    df1 = df.melt(var_name='group', value_name='value')
    # print(df1)
    # print(df)
    # perform one-way ANOVA
    result = pg.anova(data=df.melt(var_name='group', value_name='value'), dv='value', between='group')

    # print the result
    print(result.to_latex())
    print(remote[remote['color'] == 'red']['number_remote'].describe().to_latex())
    print(remote[remote['color'] == 'blue']['number_remote'].describe().to_latex())
    print(remote[remote['color'] == 'red&blue']['number_remote'].describe().to_latex())
    # print(n, j, k)
    print('______________________________________________________________________-')
