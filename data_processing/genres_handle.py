#将genres列中的数据拆成不同的行
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

#读取movies.csv并载入DataFrame中
movies=pd.read_csv('movies.csv')

#去掉genres缺失的条目
movies['remain']=movies['genres'].notnull()
movies=movies[movies['remain']]

#将movies中的genres列拆成多列，每个风格一列
genres_split=movies['genres'].apply(lambda x: Series(x.split('|')))
genres_split.columns=['genre_1','genre_2','genre_3','genre_4','genre_5']

#将新拆分的风格DataFrame和原数据中的发行年份及利润沿index方向轴向连接，形成新的数据
movies_by_genre=pd.concat([movies[['release_year','revenue_adj']],genres_split],axis=1)


#将含有不同列的genre数据的行转换成每行含有一个genre数据的若干行
movies_by_genre_melt=movies_by_genre.melt(id_vars=['release_year','revenue_adj'],value_vars=['genre_1','genre_2','genre_3','genre_4','genre_5'],value_name='genre')
#去掉genre为空的行，并保存数据
movies_by_genre_melt=movies_by_genre_melt[movies_by_genre_melt['genre'].notnull()]
movies_by_genre_melt.to_csv('movies_by_genre.csv',index=False)