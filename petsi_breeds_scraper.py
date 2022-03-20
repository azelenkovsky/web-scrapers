from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import requests
import pickle
from xml.etree import ElementTree as et
import codecs
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import numpy as np
from tabulate import tabulate
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy as db


options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument('-allow-running-insecure-content')

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 5)

driver.get("https://petsi.net/dog-breeds")

links = [x.get_attribute('href') for x in driver.find_elements_by_class_name('page-dog-breeds__list-item-title')]
breeds_array = []

print(datetime.datetime.now())

counter = 0

for link in links:
    driver.get(link)
    dictlst = {}

    breed_table_info = driver.find_element_by_class_name('breed-view__table-info').find_elements_by_tag_name('tr')
    specifications_row = driver.find_elements_by_class_name('param-dot-pane-item')
    breed_content_items = driver.find_elements_by_class_name('breed-view__content-item')
    breed_photos = driver.find_elements_by_class_name('breed-view__base-img')

    #########################################################
    # dog table info
    #########################################################

    breed_name_rus = driver.find_element_by_class_name('header-view-v1__text-wrapper').find_element_by_tag_name('h1').text
    breed_name_eng = driver.find_element_by_class_name('header-view-v1__text-wrapper').find_element_by_tag_name('h2').text

    dictlst['Название породы (рус)'] = breed_name_rus
    dictlst['Название породы (англ)'] = breed_name_eng

    #########################################################
    # dog table info
    #########################################################

    for k in range(len(breed_table_info)):

        take_value = driver.find_element_by_class_name('breed-view__table-info').find_elements_by_tag_name('tr')[k].find_elements_by_tag_name('td')
        row_dimension = take_value[0].text
        row_value = take_value[1].text

        dictlst[row_dimension] = row_value

    #########################################################
    # dog specifications
    #########################################################

    for k in range(len(specifications_row)):

        specifications_row_dimension = driver.find_elements_by_class_name('param-dot-pane-item')[k].find_element_by_class_name('param-dot-pane-item__label').text
        specifications_row_value = driver.find_elements_by_class_name('param-dot-pane-item')[k].find_element_by_class_name('param-dot-pane-item__value').find_element_by_tag_name("span").find_element_by_tag_name("span").get_attribute("class")

        specifications_row_value = int(specifications_row_value.rsplit('-', 1)[-1])

        dictlst[specifications_row_dimension] = specifications_row_value

    #########################################################
    # dog content info
    #########################################################

    for k in range(len(breed_content_items)):

        content_item_dimension = driver.find_elements_by_class_name('breed-view__content-item')[k].find_element_by_tag_name('h3').text
        content_item_value = driver.find_elements_by_class_name('breed-view__content-item')[k].find_element_by_tag_name('div').text

        dictlst[content_item_dimension] = content_item_value

    #########################################################
    # dog image url
    #########################################################

    for k in range(len(breed_photos)):

        content_item_value = driver.find_elements_by_class_name('breed-view__base-img')[k].find_element_by_tag_name('meta').get_attribute("content")
        dictlst['Ссылка на фото породы'] = content_item_value

    counter += 1

    print('Порода {0} спарсилось'.format(dictlst['Название породы (рус)']))

    breeds_array.append(dictlst)

print(datetime.datetime.now())

df_ready = pd.DataFrame(breeds_array)
df_ready.head(10)

def get_start_price(x):
    modify_from_total_price = 0
    try:
        modify_from_total_price = int(str(x).replace(" $", "").split(' - ')[0]) * 70
    except:
        pass
    return modify_from_total_price

def get_end_price(x):
    modify_from_total_price = 0
    try:
        modify_from_total_price = int(str(x).replace(" $", "").split(' - ')[1]) * 70
    except:
        pass
    return modify_from_total_price

df_ready['Цена (от)'] = df_ready['Цена'].apply(get_start_price)
df_ready['Цена (до)'] = df_ready['Цена'].apply(get_end_price)

dict_on_eng = {
    'Название породы (рус)': 'breed_name_rus',
    'Название породы (англ)': 'breed_name_eng',
    'Страна': 'country',
    'Продолжительность жизни': 'lifetime',
    'Высота': 'height',
    'Вес': 'weight',
    'Длинна шерсти': 'coat_length',
    'Цвет': 'color',
    'Группа': 'class',
    'Цена': 'price',
    'Популярность': 'popularity',
    'Тренировка': 'coaching',
    'Размер': 'size',
    'Разум': 'intellect',
    'Охрана': 'guard',
    'Отношения с детьми': 'relationships_with_children',
    'Ловкость': 'agility',
    'Линяние': 'moult',
    'История': 'history',
    'Описание': 'description',
    'Личность': 'personality',
    'Обучение': 'training',
    'Уход': 'care',
    'Распространенные заболевания': 'common_diseases',
    'Ссылка на фото породы': 'photo_url',
    'Стрижка': 'haircut',
    'Полезность': 'helpfulness',
    'Цена (от)': 'start_price',
    'Цена (до)': 'end_price'
}

df_ready.rename(columns = dict_on_eng, inplace = True)

df_ready = df_ready[['breed_name_rus', 'breed_name_eng', 'country', 'lifetime', 'height',
       'weight', 'coat_length', 'color', 'class', 'price', 'popularity', 'coaching',
       'size', 'intellect', 'guard', 'relationships_with_children',
       'agility', 'moult', 'history', 'description', 'personality', 'training',
       'care', 'common_diseases', 'photo_url', 'haircut', 'helpfulness',
       'start_price', 'end_price']]

my_conn = create_engine("your_mysql_connection_host_with_credentials")
# connection = engine.connect()

df_ready.to_sql(con = my_conn, name='dogs_info', if_exists='replace',index=False)
df_ready.head()

df_ready.to_csv('check_breeds_new_with_image.csv')

engine = create_engine("your_mysql_connection_host_with_credentials")
connection = engine.connect()
metadata = db.MetaData()
dog_friends_table = db.Table('dogs_info', metadata, Column('breed_name_rus', Integer, primary_key = True), autoload=True, autoload_with=engine)

query = '''
select *
from dogs_info
'''

ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()

connection.close()

# array_of_rus_breeds = []

# for i in ResultSet:
#     array_of_rus_breeds.append(i[0])

# print(array_of_rus_breeds)
columns_breeds = ['breed_name_rus', 'breed_name_eng', 'country', 'lifetime', 'height',
       'weight', 'coat_length', 'color', 'class', 'price', 'popularity',
       'coaching', 'size', 'intellect', 'guard', 'relationships_with_children',
       'agility', 'moult', 'history', 'description', 'personality', 'training',
       'care', 'common_diseases', 'photo_url', 'haircut', 'helpfulness',
       'start_price', 'end_price']

pd.DataFrame(ResultSet, columns = columns_breeds)

import pandas as pd
df = pd.read_csv('check_breeds.csv')

# df.columns
df[df['Название породы (рус)'] == 'Австралийская овчарка (Аусси)']['История'][0]

def start(update, context):

    me = context.bot.get_me()

    # Welcome message
    msg = "Добрый день!\n"
    msg += "Меня зовут {0} и я знаю все о породах собак.\n".format(me.first_name)
    msg += "Выберите в меню ниже интересующую вас категорию\n"

    button_list = [
        [KeyboardButton('🐶Все о породе'), KeyboardButton('🔝Рейтинг пород')],
        [KeyboardButton('📷Фотосессия собаки'), KeyboardButton('🎁Боксы для собак')],
        [KeyboardButton('🦮Изображение собак'), KeyboardButton('🏠Главное меню')]
    ]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    context.bot.send_message(chat_id=update.message.chat_id,
                     text=msg,
                     reply_markup=reply_markup)

# defs to show content
def get_one_breed_test_info(update,context):
    query = update.callback_query
#    query.answer()
#    print(query)
    context.bot.send_message(chat_id=query.message.chat_id, text='привет123')

def echo(update, context):
    """
    message to handle any "Option [0-9]" Regrex.
    """
    # sending the reply message with the selected option
    print(update)
#    update.message.reply_text("You just clicked on '%s'" % update.message.text)
    context.bot.send_message(chat_id=update.message.chat_id, text='привет123')
    pass



############################# Handlers #########################################

def main():
    updater = Updater('your_telegram_bot_token_here', use_context=True) # Токен API к Telegram
    dp = updater.dispatcher

    # support handlers
    dp.add_handler(CommandHandler('start', start))
#    dp.add_handler(MessageHandler(Filters.text, get_one_breed_test_info),group=0)
    dp.add_handler(MessageHandler(Filters.regex(r"start"), echo))
    dp.add_handler(MessageHandler(Filters.regex(r"🐶Все о породе"), echo))
#    dp.add_handler(CallbackQueryHandler(get_one_breed_test_info, pattern='get_breed_info'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
