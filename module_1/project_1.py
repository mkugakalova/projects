#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import itertools as it
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


# In[2]:


data = pd.read_csv('movie_bd_v5.csv')
data.sample(5)


# In[3]:


data.describe()


# # Предобработка

# In[4]:


answers = {}  # создадим словарь для ответов


def get_number_of_elements(list):
    """Функция для подсчета элементов списка"""
    count = 0
    for element in list:
        count += 1
    return count

# считаем прибыль/убытки фильма
data['profit'] = data['revenue'] - data['budget']
data['release_date'] = pd.to_datetime(data['release_date'])
data['release_month'] = pd.DatetimeIndex(data['release_date']).month
data['vote_average'] = pd.to_numeric(data['vote_average'])

data.head()


# # 1. У какого фильма из списка самый большой бюджет?

# In[5]:


answers['1'] = 'Pirates of the Caribbean: On Stranger Tides (tt1298650)'  # +


# In[6]:


data[data.budget == data.budget.max()][['original_title', 'imdb_id']].    reset_index(drop=True)


# # 2. Какой из фильмов самый длительный (в минутах)?

# In[7]:


answers['2'] = 'Gods and Generals (tt0279111)'  # +


# In[8]:


data[data.runtime == data.runtime.max()][['original_title', 'imdb_id']].    reset_index(drop=True)


# # 3. Какой из фильмов самый короткий (в минутах)?
# 
# 
# 
# 

# In[9]:


answers['3'] = 'Winnie the Pooh (tt1449283)'  # +


# In[10]:


data[data.runtime == data.runtime.min()][['original_title', 'imdb_id']].    reset_index(drop=True)


# # 4. Какова средняя длительность фильмов?
# 

# In[11]:


answers['4'] = '110'  # +


# In[12]:


int(round(data.runtime.mean(), 0))


# # 5. Каково медианное значение длительности фильмов? 

# In[13]:


answers['5'] = '107'  # +


# In[14]:


int(round(data.runtime.median(), 0))


# # 6. Какой самый прибыльный фильм?
# #### Внимание! Здесь и далее под «прибылью» или «убытками» понимается разность между сборами и бюджетом фильма. (прибыль = сборы - бюджет) в нашем датасете это будет (profit = revenue - budget) 

# In[15]:


answers['6'] = 'Avatar (tt0499549)'  # +


# In[16]:


data[data.profit == data.profit.max()][['original_title', 'imdb_id']].    reset_index(drop=True)


# # 7. Какой фильм самый убыточный? 

# In[17]:


answers['7'] = 'The Lone Ranger (tt1210819)'  # +


# In[18]:


data[data.profit == data.profit.min()][['original_title', 'imdb_id']].    reset_index(drop=True)


# # 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?

# In[19]:


answers['8'] = '1478'  # +


# In[20]:


data[data.profit > 0].imdb_id.nunique()


# # 9. Какой фильм оказался самым кассовым в 2008 году?

# In[21]:


answers['9'] = 'The Dark Knight (tt0468569)'  # +


# In[22]:


data_9 = data[data.release_year == 2008].reset_index()
data_9[data_9.revenue == data_9.revenue.max()][
    ['original_title', 'imdb_id']].reset_index(drop=True)


# # 10. Самый убыточный фильм за период с 2012 по 2014 г. (включительно)?
# 

# In[23]:


answers['10'] = 'The Lone Ranger (tt1210819)'  # +


# In[24]:


data_10 = data[(data.release_year >= 2012) & (data.release_year <= 2014)].    reset_index()
data_10[data_10.profit == data_10.profit.min()][
    ['original_title', 'imdb_id']].reset_index(drop=True)


# # 11. Какого жанра фильмов больше всего?

# In[25]:


answers['11'] = 'Drama'  # +


# In[26]:


data_11 = data.genres.str.split('|').explode().value_counts().    sort_values(ascending=False).reset_index()
data_11.columns = ['genre', 'movies_cnt']
data_11.head(1)


# # 12. Фильмы какого жанра чаще всего становятся прибыльными? 

# In[27]:


answers['12'] = 'Drama'  # +


# In[28]:


data_12 = data[data.profit > 0].genres.str.split('|').    explode().value_counts().sort_values(ascending=False).reset_index()
data_12.columns = ['genre', 'movies_cnt']
data_12.head(1)


# # 13. У какого режиссера самые большие суммарные кассовые сборы?

# In[29]:


answers['13'] = 'Peter Jackson'  # +


# In[30]:


data.groupby(['director'])['revenue'].sum().reset_index().sort_values(
    by='revenue', ascending=False).head(1)


# # 14. Какой режисер снял больше всего фильмов в стиле Action?

# In[31]:


answers['14'] = 'Robert Rodriguez'  # +


# In[32]:


data_14 = data[data.genres.str.contains('Action')].    director.str.split('|').explode().value_counts().    reset_index().nlargest(1, 'director')
data_14.columns = ['director', 'movies_cnt']
display(data_14)


# # 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году? 

# In[33]:


answers['15'] = 'Chris Hemsworth'  # +


# In[34]:


data_15 = data[data.release_year == 2012][
    ['release_year', 'cast', 'revenue']].reset_index(drop=True)
data_15['cast'] = data_15.cast.str.split('|')
data_15 = data_15.explode('cast')
data_15.groupby(['cast'])['revenue'].sum().reset_index().sort_values(
    by='revenue', ascending=False).head(1)


# # 16. Какой актер снялся в большем количестве высокобюджетных фильмов?

# In[35]:


answers['16'] = 'Matt Damon'  # +


# In[36]:


data_16 = data[data.budget > data.budget.mean()].    reset_index(drop=True)
data_16['cast'] = data_16.cast.str.split('|')
data_16 = data_16.explode('cast')
data_16.groupby('cast')['imdb_id'].nunique().    reset_index().sort_values(by='imdb_id', ascending=False).head(1)


# # 17. В фильмах какого жанра больше всего снимался Nicolas Cage? 

# In[37]:


answers['17'] = 'Action'  # +


# In[38]:


data_17 = data[data.cast.str.contains('Nicolas Cage')][
    ['imdb_id', 'genres', 'cast']]
data_17['genres'] = data_17.genres.str.split('|')
data_17 = data_17.explode('genres')
data_17 = data_17.groupby('genres')['imdb_id'].nunique().reset_index()
data_17.columns = ['genres', 'movies_cnt']
data_17.sort_values(by='movies_cnt', ascending=False).head(1)


# # 18. Самый убыточный фильм от Paramount Pictures

# In[39]:


answers['18'] = 'K-19: The Widowmaker (tt0267626)'  # +


# In[40]:


# все фильмы Paramount Pictures
data_18 = data[data.production_companies.str.contains('Paramount Pictures')]
# фильм с самой низкой прибылью
data_18[data_18.profit == data_18.profit.min()][
    ['original_title', 'imdb_id']].reset_index(drop=True)


# # 19. Какой год стал самым успешным по суммарным кассовым сборам?

# In[41]:


answers['19'] = '2015'  # +


# In[42]:


data.groupby('release_year').revenue.sum().reset_index().    sort_values(by='revenue', ascending=False).head(1)


# # 20. Какой самый прибыльный год для студии Warner Bros?

# In[43]:


answers['20'] = '2014'  # +


# In[44]:


# все фильмы Warner Bros.
data_20 = data[data.production_companies.str.contains('Warner Bros')]
data_20.groupby('release_year').profit.sum().reset_index().    sort_values(by='profit', ascending=False).head(1)


# # 21. В каком месяце за все годы суммарно вышло больше всего фильмов?

# In[45]:


answers['21'] = '9'  # +


# In[46]:


data_21 = data.groupby('release_month').imdb_id.nunique().    reset_index().sort_values(by='imdb_id', ascending=False)
data_21.columns = ['release_month', 'movie_cnt']
data_21.head(1)


# # 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)

# In[47]:


answers['22'] = '450'  # +


# In[48]:


data[data.release_month.isin([6, 7, 8])].imdb_id.nunique()


# # 23. Для какого режиссера зима – самое продуктивное время года? 

# In[49]:


answers['23'] = 'Peter Jackson'  # +


# In[50]:


data_23 = data[data.release_month.isin([12, 1, 2])]  # все "зимние" фильмы
data_23 = data_23.director.str.split('|').explode().value_counts().    reset_index().nlargest(1, 'director')
data_23.columns = ['director', 'movies_cnt']
display(data_23)


# # 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?

# In[51]:


answers['24'] = 'Four By Two Productions'  # +


# In[52]:


data_24 = data.copy()
data_24['production_companies'] = data_24.production_companies.str.split('|')
data_24 = data_24.explode('production_companies')
data_24['original_title_len'] = data_24['original_title'].str.len()
data_24.groupby('production_companies')['original_title_len'].    mean().reset_index().sort_values(by='original_title_len',
                                        ascending=False).head(1)


# # 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?

# In[53]:


answers['25'] = 'Midnight Picture Show'  # +


# In[54]:


data_25 = data.copy()
data_25['production_companies'] = data_25.production_companies.str.split('|')
data_25 = data_25.explode('production_companies')
data_25['overview_words_count'] = data_25['overview'].    str.split().apply(get_number_of_elements)  # считаем количество слов
data_25.groupby('production_companies')['overview_words_count']    .mean().reset_index().sort_values(by='overview_words_count',
                                      ascending=False).head(1)


# # 26. Какие фильмы входят в 1 процент лучших по рейтингу? 
# по vote_average

# In[55]:


answers['26'] = 'The Dark Knight, Inside Out, 12 Years a Slave'  # +


# In[56]:


large = int(round(data.imdb_id.nunique()/100, 0))  # расчитываем 1% значений
data[['original_title', 'vote_average']].reset_index(drop=True).    nlargest(large, columns='vote_average')


# # 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# 

# In[57]:


answers['27'] = 'Daniel Radcliffe, Rupert Grint'  # +


# In[58]:


data_27 = data.cast.str.split('|').reset_index()
data_27 = data_27.cast.apply(lambda x: list(it.combinations(x, 2)))
data_27.explode().mode()


# # Submission

# In[59]:


# в конце можно посмотреть свои ответы к каждому вопросу
answers


# In[60]:


# и убедиться что ни чего не пропустил)
len(answers)

