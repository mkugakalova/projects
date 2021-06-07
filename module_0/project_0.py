#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

def game_core_v3(number):
    '''Функция, реализующая бинарный поиск: 
    на каждом шаге определяем слева или справа от середины находится загаданное число.
    Функция принимает загаданное число и возвращает число попыток'''

    predict = np.random.randint(1,101) # загадываем случайное число

    #создаем список, по которому будем искать
    number_list = []
    for number in range(1, 101): 
        number_list.append(number)

    #задаем начальные значения индексов середины, начала и конца интервала поиска
    mid_index = len(number_list) // 2
    min_index = 0
    max_index = len(number_list) - 1

    count = 1 # инициализируем счетчик попыток
    while number_list[mid_index] != predict:  # значение из середины интервала не равно искомому
        count += 1 # увеличиваем счетчик попыток
        if predict > number_list[mid_index]: 
            # если искомое число больше числа из середины интервала, то смещаем границу интервала вправо от середины
            min_index = mid_index + 1
        else:
             # иначе, смещаем границу интервала влево от середины
            max_index = mid_index - 1 
        mid_index = (min_index+max_index) // 2 # определяем новую середину интервала
        

    return(count) # выход из цикла, если угадали


def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    
    return(score)


# Проверяем
score_game(game_core_v3)

