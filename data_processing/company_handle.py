#整理筛选出Universal Pictures 和 Paramount Pictures 的数据，并保存
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
#读取movies.csv并载入DataFrame中
movies=pd.read_csv('movies.csv')

#去掉production_companies缺失、budget_adj缺失以及revenue_adj缺失的条目
movies['remain']= movies['production_companies'].notnull() & (movies['budget_adj']!=0) & (movies['revenue_adj']!=0)
movies=movies[movies['remain']]

#将movies中的production_companies列拆成多列，每个公司一列
companies_split=movies['production_companies'].apply(lambda x: Series(x.split('|')))
companies_split.columns=['company_1','company_2','company_3','company_4','company_5']

#将新拆分的公司DataFrame和原数据中的导演、发行年份、预算及利润沿index方向轴向连接，形成新的数据
movies_by_company=pd.concat([movies[['director','release_year','budget_adj','revenue_adj']],companies_split],axis=1)

#将含有不同公司数据的行转换成每行含有一个公司数据的若干行
movies_by_company_melt=movies_by_company.melt(id_vars=['director','release_year','budget_adj','revenue_adj'],value_vars=['company_1','company_2','company_3','company_4','company_5'],value_name='company')

#选出company中的值为Universal Pictures 或 Paramount Pictures的行，并保存

in_Universa_Pictures=movies_by_company_melt['company']=='Universal Pictures'
in_Paramount_Pictures=movies_by_company_melt['company']=='Paramount Pictures'

movies_by_company_melt=movies_by_company_melt[in_Universa_Pictures | in_Paramount_Pictures]
movies_by_company_melt.to_csv('movies_by_company.csv',index=False)



#再去掉director缺失的条目
movies_by_company_melt['remain']=movies_by_company_melt['director'].notnull()
movies_two_company=movies_by_company_melt[movies_by_company_melt['remain']]

#将movies_two_company中的director拆成多列，每个导演一列
director_split=movies_two_company['director'].apply(lambda x:Series(x.split('|')))
director_split.columns=['director_1','director_2','director_3']

#将新拆分的导演DataFrame和movies_two_company中的公司及利润沿index方向连接，形成新数据
movies_by_director=pd.concat([movies_two_company[['company','revenue_adj']],director_split],axis=1)

#将含有不同导演数据的行转换成每行含有一个公司数据的若干行
movies_by_director_melt=movies_by_director.melt(id_vars=['company','revenue_adj'],value_vars=['director_1','director_2','director_3'],value_name='director')
movies_by_director_melt=movies_by_director_melt[movies_by_director_melt['director'].notnull()]

#将数据按公司和导演名称进行聚合，分别计算两个公司每个导演拍片总量
movies_per_director=movies_by_director_melt.groupby(['company','director'],as_index=False)['variable'].count()

#分别找出每个公司拍片量前10的导演，再将数据合并在一起，并将数据保存
UP_top10=movies_per_director[movies_per_director['company']=='Universal Pictures'].sort_values(by='variable',ascending=False)[:10]
PP_top10=movies_per_director[movies_per_director['company']=='Paramount Pictures'].sort_values(by='variable',ascending=False)[:10]
director_top10 = pd.concat([UP_top10,PP_top10])

#director_top10.to_csv('director_top10.csv')