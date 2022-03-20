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

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

import time

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 5)

driver.get("https://propala.ru/adverts/lost-dog/1/")

# find last page id for lost dogs in propala.ru
low_menu = driver.find_element_by_class_name('pagination')
low_menu_list = driver.find_elements_by_tag_name('li')
array_of_pages = []

for i in low_menu_list:
    try:
        array_of_pages.append(int(i.text))
    except:
        pass

max_page_id = max(array_of_pages)
print(max_page_id)

# make array of available pages
array_of_page_links = []
for i in range(1, max_page_id + 1):
    add_page_link = "https://propala.ru/adverts/lost-dog/1/page/{}/".format(str(i))
    array_of_page_links.append(add_page_link)


# print(array_of_page_links)

array_of_all_links = []

# iterate through pages of lost dogs
for i in array_of_page_links:

    print("Begin scrape {0}".format(i))

    # begin scraping of each page
    driver.get(i)
    dog_blocks = driver.find_elements_by_class_name('col-lg-4')

    for n in dog_blocks:
        link_of_certain_dog = str(n.find_element_by_tag_name('a').get_attribute("href"))
        if 'view' in link_of_certain_dog:
            array_of_all_links.append(link_of_certain_dog)

print(array_of_all_links)

import datetime

full_array_of_dictionaries = []

print(datetime.datetime.now())

counter_links = 0

for i in array_of_all_links:

    # get all pages
    print(i)
    driver.get(i)

    # get_main_block
    dog_main_block = driver.find_element_by_css_selector(".col-lg-12.classified.ui-block")

    # get dog photo
    try:
        dog_photo = str(dog_main_block.find_element_by_tag_name('img').get_attribute('src'))
    except:
        dog_photo = "no photo uploaded"
    # get details info

    # iterate through blocks
    classified_details_blocks = dog_main_block.find_elements_by_class_name("classified_details")

    # dictionary of full info
    dictionary_of_details = {}
    counter = 0

    # find owner name
    owner_name = driver.find_element_by_class_name("ui-block-title")
    array_owner_name = owner_name.text.split('\n')
    dictionary_of_details['owner_name'] = array_owner_name[0]
    dictionary_of_details['ads_date'] = array_owner_name[1]

    # find owner phone
    owner_phone = driver.find_element_by_class_name("ui-block-content").find_element_by_class_name("pull-left")
    array_owner_phone = owner_phone.text.split('\n')
    dictionary_of_details['owner_phone'] = array_owner_phone[1]

    for n in classified_details_blocks:
        try:
            if counter == 0:
                dictionary_of_details['full_ad_text'] = n.text
                counter += 1

            else:
                blocks = n.find_elements_by_tag_name("div")
                for m in blocks:
                    array_detail_block = m.text.split('\n')

                    dictionary_of_details[array_detail_block[0]] = array_detail_block[1]

                counter += 1

        except:
            pass

    dictionary_of_details['photo_url'] = dog_photo
    dictionary_of_details['website_url'] = i

    full_array_of_dictionaries.append(dictionary_of_details)

    counter_links += 1

# driver.quit()

print(datetime.datetime.now())
print("Total parsed ads - {0}".format(counter_links))

df_ready = pd.DataFrame(full_array_of_dictionaries)
print(df_ready)

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

import time
# options.add_argument("--remote-debugging-port=9222")
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument('-allow-running-insecure-content')

driver = webdriver.Chrome(options=options)
driver.maximize_window()

wait = WebDriverWait(driver, 5)

driver.get("https://propala.ru/adverts/lost-dog/1/")
# driver.get("https://petsi.net/dog-breeds")

# get_div = driver.find_element_by_xpath('//*[@id="drwbtn"]').click()
# time.sleep(20)
# get_div.text

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="drwbtn"]')))
element.click()

large_sector = driver.find_element_by_css_selector('.p-sitemap__nav.b-sitemap__list')
large_sector_list = large_sector.find_elements_by_tag_name('li')

list_all_sector_links = []

for i in large_sector_list:
    try:
        list_all_sector_links.append(str(i.find_element_by_tag_name('a').get_attribute("href")))
    except:
        pass

print(list_all_sector_links)

ready_list = []

for link in list_all_sector_links[0:]:
    print('Начинаем парсинг раздела - {}'.format(link))
    driver.get(link)

#     element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="drwbtn"]')))
#     element.click()

    sector_cols = driver.find_elements_by_css_selector('.col-xs-4.b-sitemap')

    for m in sector_cols:
        li_array = m.find_elements_by_tag_name('li')

        for n in li_array:
            dictlst = {}
            zhk_avaho_link = str(n.find_element_by_tag_name('a').get_attribute("href"))
            zhk_avaho_name = str(n.text)
            dictlst['zhk_name'] = zhk_avaho_name
            dictlst['zhk_url'] = zhk_avaho_link
            ready_list.append(dictlst)

driver.quit()

df_ready = pd.DataFrame(ready_list)
print(df_ready)


# работающий код на парсинг названий и ссылок на жк
# sector_cols = driver.find_elements_by_css_selector('.col-xs-4.b-sitemap')

# dictlst = {}
# ready_list = []

# for m in sector_cols:
#     li_array = m.find_elements_by_tag_name('li')
#     for n in li_array:
#         dictlst = {}
#         zhk_avaho_link = str(n.find_element_by_tag_name('a').get_attribute("href"))
#         zhk_avaho_name = str(n.text)
#         dictlst['zhk_name'] = zhk_avaho_name
#         dictlst['zhk_url'] = zhk_avaho_link
#         ready_list.append(dictlst)


# df_ready = pd.DataFrame(ready_list)
# df_ready

# конец работающий код на парсинг названий и ссылок на жк

# print(elem.get_attribute("href"))

# sector_cols = driver.find_elements_by_class_name('b-sitemap__list')

# # sector_cols

# for m in sector_cols:
#     li_array = m.find_elements_by_tag_name('li')
#     for n in li_array:
#         print(n.text)

# driver.find_element_by_tag_name('body').text
# zkh_values = driver.find_elements_by_tag_name('li')

# print(zkh_values)
# for i in zkh_values:
#     print(i.text)

# lang = driver.find_element_by_class_name("b-title")

# langs = driver.find_element_by_xpath("//*[@class='b-title']")

# print(langs[0].text)
# print(lang.text)

# for lang in langs:
#     print(lang.text)

# zhk_columns_list = driver.find_element_by_class_name('p-sitemap__content')
# zhk_columns_list
# array_of_values = []

# for k in range(len(zhk_columns_list)):
#     all_rows_in_avaho = driver.find_elements_by_class_name('col-xs-4 b-sitemap')[k].find_elements_by_tag_name('li')[0].text
#     print(all_rows_in_avaho)
#     for m in range(len(all_rows_in_avaho)):
#         print(all_rows_in_avaho[m].text)

zhk_info = []

driver = webdriver.Chrome(options=options)

for i in ready_list:
    print('Begin uploading - {}'.format(i['zhk_name']))
    driver.get(str(i['zhk_url']))
    if i['zhk_name'] == 'ЖК Аалто':
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="drwbtn"]')))
        element.click()
#     except:
#         pass

    zhk_characteristics = {}

    zhk_characteristics['zhk_name'] = i['zhk_name']
    zhk_characteristics['zhk_url'] = i['zhk_url']

    # get xhk geodata
    geo_data = driver.find_elements_by_class_name('geo-field')
    for m in geo_data:
#        print('{0} - {1}'.format(i['zhk_name'], m.text))
        # begin parsing geo data
        try:
            zhk_info_key = m.text.split(':', 1)[0]
            zhk_info_value = m.text.split(':', 1)[1]
            zhk_characteristics[zhk_info_key] = zhk_info_value
        except:
            pass

    # get zhk details
    details_data = driver.find_elements_by_class_name('opt-field')
    for n in details_data:
#        print('{0} - {1}'.format(i['zhk_name'], m.text))
        # begin parsing details data
        try:
            zhk_info_key = n.text.split(':', 1)[0]
            zhk_info_value = n.text.split(':', 1)[1]
            zhk_characteristics[zhk_info_key] = zhk_info_value
        except:
            pass

    try:
        zhk_characteristics['avaho_rating'] = float(driver.find_element_by_class_name('mc-rate').text)
    except:
        zhk_characteristics['avaho_rating'] = 0.0

    print(zhk_characteristics)

    zhk_info.append(zhk_characteristics)
#     except:
#         pass

df_zhk_info = pd.DataFrame(zhk_info)
print(df_zhk_info)

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

for link in links:
    driver.get(link)
    dictlst = {}

    breed_table_info = driver.find_element_by_class_name('breed-view__table-info').find_elements_by_tag_name('tr')
    specifications_row = driver.find_elements_by_class_name('param-dot-pane-item')
    breed_content_items = driver.find_elements_by_class_name('breed-view__content-item')

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


    breeds_array.append(dictlst)

df_ready = pd.DataFrame(breeds_array)
df_ready.head(10)

#/usr/bin/python3.6
# coding: utf-8
import pandas as pd
import numpy as np
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler,Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Bot
from telegram.ext import Updater
import datetime
import logging
import time

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
