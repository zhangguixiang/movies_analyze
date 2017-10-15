#清理vote_average，budget_adj，revenue_adj缺失的记录
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

#读取movies.csv并载入DataFrame中
movies=pd.read_csv('movies.csv')

#去掉vote_average，budget_adj，revenue_adj缺失缺失的条目
movies['remain']=(movies['vote_average']!=0)& (movies['budget_adj']!=0) & (movies['revenue_adj']!=0)
movies=movies[movies['remain']]

#将清理后的movies记录保存为movies_cleaned.csv
movies.to_csv('movies_cleaned.csv',index=False)