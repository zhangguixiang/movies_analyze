#将电影分为改编和原创
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

#读取movies.csv并载入DataFrame中
movies=pd.read_csv('movies.csv')

#去掉keywords缺失的条目
movies['remain']=movies['keywords'].notnull()
movies=movies[movies['remain']]

#识别每个电影是否是原创，并添加一列original用来记录

def is_original(df):
	return 'based on novel' not in df.split('|')

movies['original']=movies['keywords'].apply(is_original)

#计算每年原创和非原创的电影比例，并将结果保存为movies_original_percent.csv
pivoted=movies.pivot_table('budget_adj',index='release_year',columns='original',aggfunc='count',fill_value=0)
movies_original_percent=DataFrame([])
movies_original_percent['original']=pivoted[True]/pivoted.sum(axis=1)
movies_original_percent['not_original']=pivoted[False]/pivoted.sum(axis=1)
movies_original_percent.to_csv('movies_original_percent.csv')

#去掉vote_average，budget_adj，revenue_adj缺失的条目
movies['remain']=(movies['vote_average']!=0)& (movies['budget_adj']!=0) & (movies['revenue_adj']!=0)
movies=movies[movies['remain']]

#将增加了原创标记列的数据保存为movies_original.csv
movies.to_csv('movies_original.csv',index=False)

