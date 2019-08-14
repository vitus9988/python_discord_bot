import discord
from selenium import webdriver
from bs4 import BeautifulSoup
import bs4
from urllib.request import urlopen
import urllib
import urllib.request
import os
import requests
import sys
import io
import random
from googletrans import Translator
import time
import re
import subprocess
import pandas as pd
import ssl
import datetime
from collections import Counter
from gensim.summarization.summarizer import summarize
import numpy as np
from newspaper import Article

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


def main():
    app = discord.Client()

    @app.event
    async def on_ready():
        print('Logged in as')
        print(app.user.name)
        print(app.user.id)
        print('+++++++++++++')
        await app.change_presence(game=discord.Game(name='크롤링', type=1))

    @app.event
    async def on_reaction_add(reaction, user):
        channel = reaction.message.channel
        await app.send_message(channel,
                               '{}가 {}에 {} 이모지를 달았습니다.'.format(user.name, reaction.message.content, reaction.emoji))

    @app.event
    async def on_reaction_remove(reaction, user):
        channel = reaction.message.channel
        await app.send_message(channel,
                               '{}가 {}에 {} 이모지를 제거'.format(user.name, reaction.message.content, reaction.emoji))

    # ㅇㅇㅇ

    @app.event
    async def on_message(message):

        ####봇 dm 테스트코드
        if message.content.startswith('whoami'):
            user_id = message.author.id
            user_name = message.author.name
            txt = '{} {}'.format(user_id, user_name)
            await app.send_message(message.channel, txt)

        if message.content.startswith('!제어'):
            user_id = message.author.id
            sentence = message.content.split(' ')
            word = ''.join(sentence[1:])

            if user_id == '123456789':
                # bot_developer_id
                if word == 'pwd':
                    n_dir = os.getcwd()
                    await app.send_message(message.channel, n_dir)
                elif word == 'll':
                    f = open('output.txt', 'w')
                    output = subprocess.check_output(['ls -alh'], shell=True, encoding='utf-8')

                    f.write(output)
                    f.close()
                    embed = discord.Embed(
                        title='ls -alh',
                        color=discord.Color.red())
                    with open('output.txt') as t:
                        for i in t:
                            embed.add_field(name='결과', value='{}\n'.format(i))
                    await app.send_message(message.channel, embed=embed)
            else:
                await app.send_message(message.channel, 'permission denied')

        if message.content.startswith('!기억'):
            m_sentence = message.content.split(' ')
            memories = ' '.join(m_sentence[1:])
            u_id = message.author.id
            m_file = open('memory.txt', 'a', encoding='utf8')
            lines = u_id + ': ' + memories + '\n'
            m_file.write(lines)
            m_file.close()
            await app.send_message(message.channel, 'ㅇㅋ')

        if message.content.startswith('!망각'):
            u_id = message.author.id
            f = open('memory.txt', 'r')
            lines = f.readlines()
            f.close()
            f = open('memory.txt', 'w')
            for i in lines:
                if u_id not in i:
                    f.write(i)
            f.close()
            await app.send_message(message.channel, '기억 삭제')

        if message.content.startswith('!회상'):
            u_id = message.author.id
            embed = discord.Embed(
                title='기억 목록',
                color=discord.Color.red()
            )
            count = 1
            with open('memory.txt') as f:
                for i in f:
                    stat = i.split(': ')
                    s_ui = ''.join(stat[0])
                    s_tx = ' '.join(stat[1:])
                    if s_ui == u_id:
                        embed.add_field(name=str(count) + '.', value='{}'.format(s_tx))
                        count += 1
            await app.send_message(message.author, embed=embed)

        if message.content.startswith('!') and message.content.endswith('연차'):
            try:
                playgames = message.content[1:-2]
                if int(playgames) >= 1001:
                    await app.send_message(message.channel,'도박문제 전화상담 서비스(국번 없이 ☎1336)')
                else:
                    g_point = 0
                    player_name = message.author.name
                    gotcha = np.random.choice(3, int(playgames), p=[0.01, 0.2, 0.79])
                    embed = discord.Embed(
                        title='{}의 {}연차'.format(player_name, playgames),
                        color=discord.Color.dark_blue()
                    )
                    for i in gotcha:
                        if i == 1:
                            g_point += 2
                        elif i == 2:
                            g_point += 1
                        else:
                            g_point += 3
                    embed.add_field(name='결과',
                                    value='1성:{}, 2성:{}, 3성:{}\n가챠포인트:{}'.format(Counter(gotcha)[2], Counter(gotcha)[1],
                                                                                 Counter(gotcha)[0], g_point))
                    gotcha_per = int(Counter(gotcha)[0]) / int(playgames) * 100
                    if gotcha_per >= 2.0:
                        await app.send_message(message.channel, embed=embed)
                        await app.send_file(message.channel, fp='img_con/icon_96.png')
                    else:
                        await app.send_message(message.channel, embed=embed)
                        gotcha_ran = ['img_con/icon_55.png', 'img_con/icon_22.png', 'img_con/icon_58.png']
                        await app.send_file(message.channel, fp=random.choice(gotcha_ran))
            except:
                await app.send_message(message.channel, 'command not found')


        if message.content.startswith('!이마트'):
            sentence = message.content.split(' ')
            mart = ' '.join(sentence[1:])
            f = open('emart.txt', 'r')
            line = f.read().splitlines()
            for i in line:
                stat = i.split(' ')
                if mart in stat and len(stat) == 2:
                    await app.send_message(message.channel, '점포명:{} 영업여부:{}'.format(stat[0], stat[-1]))
                elif mart in stat and len(stat) == 3:
                    await app.send_message(message.channel, '점포명:{} 영업여부:{}'.format(stat[0] + stat[1], stat[-1]))



        # 네이버 뉴스 사회면 출력
        if message.content.startswith('!사회'):
            embed = discord.Embed(
                title='사회면 뉴스 순위',
                color=discord.Color.red()
            )
            html = urllib.request.urlopen('https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=102')
            news_url = 'https://news.naver.com'
            soup = BeautifulSoup(html, 'lxml')
            news1 = soup.find('div', {'id': 'ranking_102'})
            news2 = news1.find('ul', 'section_list_ranking')
            news3 = news2.find_all('a', "nclicks(rig.ranksoc)")
            count = 1
            for i in news3:
                re_title = i.text
                news_href = i.get('href')
                embed.add_field(name=str(count) + '위: ', value='[%s](<%s>)' % (re_title, news_url + news_href))
                count += 1
            await app.send_message(message.channel, embed=embed)

        if message.content.startswith('!요약'):
            sentence = message.content.split(' ')
            txt_url = ''.join(sentence[1])

            news = Article(txt_url, language='ko')
            news.download()
            news.parse()
            embed = discord.Embed(
                title='url의 텍스트를 요약',
                color=discord.Color.dark_purple()
            )
            text_summ = summarize(news.text, word_count=50)
            embed.add_field(name='요약', value='[%s](<%s>)' % (text_summ, txt_url))
            await app.send_message(message.channel, embed=embed)

        if message.content.startswith('!주사위'):
            number = message.content.split(' ')
            dice_num = int(number[1])
            dice = []
            for i in range(1, dice_num + 1):
                dice.append(random.randint(1, 6))

            await app.send_message(message.channel, dice)

        if message.content.startswith('!다나와'):
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable--gpu')
            options.add_argument('–no-sandbox')
            chromedriver_dir = r'chromedriver_ver/linux/chromedriver'
            driver = webdriver.Chrome(chromedriver_dir, chrome_options=options)

            sentence = message.content.split(' ')
            word = ' '.join(sentence[1:])
            s_word = urllib.parse.quote(word)
            driver.get('http://search.danawa.com/dsearch.php?k1=' + s_word + '&module=goods&act=dispMain')
            time.sleep(3)
            source = driver.page_source
            soup = bs4.BeautifulSoup(source, 'lxml')

            stat = soup.find_all('p', 'prod_name')
            price_stat = soup.find_all('p', 'price_sect')
            driver.quit()
            embed = discord.Embed(
                title='다나와 ' + word + ' 검색결과',
                color=discord.Color.dark_purple()
            )

            count = 1
            for i, k in zip(stat, price_stat):
                title = i.text.strip()
                price = k.find('a').text.strip()
                embed.add_field(name=str(count) + '.', value='{}\n{}'.format(title, price))
                count += 1
                if count == 7:
                    break
            await app.send_message(message.channel, embed=embed)



        if message.content.startswith('!유튭'):

            sentence = message.content.split(' ')
            word = ' '.join(sentence[1:])
            search_word = urllib.parse.quote(word)
            html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + search_word)
            soup = BeautifulSoup(html, 'lxml')
            tt = soup.find('ol', 'item-section')
            stat = tt.find_all('h3', 'yt-lockup-title')

            embed = discord.Embed(
                title='유튜브 검색결과',
                color=discord.Color.blue()
            )
            count = 1
            for i in stat:
                url = 'https://www.youtube.com'
                tx = i.text
                tx = tx.split(' ')[:-3]
                ti = ' '.join(tx)
                link = i.find('a').get('href')
                embed.add_field(name=str(count) + '.', value='[%s](<%s>)' % (ti, url + link))
                count += 1
                if count == 6:
                    break
            await app.send_message(message.channel, embed=embed)

        if message.content.startswith('!파파고'):
            sentence = message.content.split(' ')
            trans_text = ''.join(sentence[1:])
            request_url = "https://openapi.naver.com/v1/papago/n2mt"
            headers = {"X-Naver-Client-Id": "123456789", "X-Naver-Client-Secret": "12345678"} # personal_token
            params = {"source": "ko", "target": "en", "text": trans_text}
            response = requests.post(request_url, headers=headers, data=params)
            result = response.json()
            await app.send_message(message.channel, result['message']['result']['translatedText'])

        if message.content.startswith('!번역'):
            sentence = message.content.split(' ')
            convert_sentence = ' '.join(sentence[1:])
            translator = Translator()
            if translator.detect(convert_sentence).lang != 'ko':
                result = translator.translate(convert_sentence, dest='ko').text
                await app.send_message(message.channel, result)
            if translator.detect(convert_sentence).lang == 'ko':
                result = translator.translate(convert_sentence, dest='en').text
                await app.send_message(message.channel, result)

        if message.content.startswith('!날씨'):
            try:
                sentence = message.content.split(' ')
                area = ' '.join(sentence[1:])
                location = urllib.parse.quote(area + '+날씨')
                html = urllib.request.urlopen(
                    'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + location)
                soup = BeautifulSoup(html, 'lxml')
                area_loca = soup.find('div', 'select_box').find('em').text
                embed = discord.Embed(
                    title=area_loca + '의 날씨정보',
                    color=discord.Color.blue()
                )

                # ------오늘 날씨 정보------------
                today_weather = soup.select(
                    '#main_pack > div.sc.cs_weather._weather > div:nth-child(2) > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.main_info')[
                    0]
                today_dust_stat = soup.select(
                    '#main_pack > div.sc.cs_weather._weather > div:nth-child(2) > div.weather_box > div.weather_area._mainArea > div.today_area._mainTabContent > div.sub_info > div > dl')[
                    0]

                today_temp = today_weather.find('span', 'todaytemp').text
                today_stat = today_weather.find('p', 'cast_txt').text
                skin_temp = today_weather.find('span', 'sensible').find('span', 'num').text

                # ------내일 날씨 정보------------
                tomm_weather = soup.select(
                    '#main_pack > div.sc.cs_weather._weather > div:nth-child(2) > div.weather_box > div.weather_area._mainArea > div:nth-child(4)')[
                    0]

                temp_am, temp_pm = tomm_weather.find_all('span', 'todaytemp')
                air_am, air_pm = tomm_weather.find_all('p', 'cast_txt')

                # ------언패킹 오류 발생 위치-----
                try:
                    t_dust = today_dust_stat.find_all('dd')
                    mise, c_mise, o_z = t_dust
                    mise_am, mise_pm = tomm_weather.find_all('div', 'detail_box')
                except ValueError:
                    embed.add_field(name='오늘',
                                    value='현재온도 : {}도, 체감온도 : {}도\n{}'.format(today_temp, skin_temp, today_stat))
                    embed.add_field(name='내일', value='오전온도 : {}도, {}\n오후온도 : {}도, {}'.format(temp_am.text, air_am.text,
                                                                                             temp_pm.text.strip(),
                                                                                             air_pm.text))
                else:
                    embed.add_field(name='오늘',
                                    value='현재온도 : {}도, 체감온도 : {}도\n{}\n미세먼지 : {}\n초미세먼지 : {}'.format(today_temp,
                                                                                                     skin_temp,
                                                                                                     today_stat,
                                                                                                     mise.text,
                                                                                                     c_mise.text))
                    embed.add_field(name='내일',
                                    value='오전온도 : {}도, {}\n{}\n오후온도 : {}도, {}\n{}'.format(temp_am.text, air_am.text,
                                                                                          mise_am.text.strip(),
                                                                                          temp_pm.text.strip(),
                                                                                          air_pm.text,
                                                                                          mise_pm.text.strip()))

                await app.send_message(message.channel, embed=embed)
                if float(skin_temp) >= 30.0 and float(skin_temp) < 35.0:
                    await app.send_file(message.channel, fp='img_con/icon_49.png')
                elif float(skin_temp) >= 35.0:
                    await app.send_file(message.channel, fp='img_con/icon_38.gif')
            except:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith("!주간날씨"):
            try:
                sentence = message.content.split(' ')
                area = sentence[1]
                location = urllib.parse.quote(area + '+날씨')
                html = urllib.request.urlopen(
                    'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + location)
                soup = BeautifulSoup(html, 'lxml')
                title = soup.find('div', 'select_box').find('em')
                week = soup.find_all('li', 'date_info')
                embed = discord.Embed(
                    title=title.text + '의 주간 날씨 정보',
                    color=discord.Color.blue()
                )
                for i in week:
                    day = i.find('span', 'day_info').text
                    am = i.find('span', 'point_time morning').text.strip()
                    pm = i.find('span', 'point_time afternoon').text.strip()
                    temp = i.find('dd').text
                    embed.add_field(name=day, value='오전:{}\n오후:{}\n{}'.format(am, pm, temp))
                await app.send_message(message.author, embed=embed)
            except:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith('!세계날씨'):
            try:
                sentence = message.content.split(' ')
                out_area = ''.join(sentence[1:])

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

                base_url = 'https://www.google.com/search?ei=2FIQXbn7OIuU8wXRtonYCA&q=' + out_area + '+날씨'
                html = requests.get(base_url, headers=headers).text
                soup = BeautifulSoup(html, 'lxml')
                stat = soup.find_all('div', 'vk_c card-section')

                for i in stat:
                    location = i.find('div', 'vk_gy vk_h').text.strip()
                    loca_time = i.find('div', 'vk_gy vk_sh').text.strip()
                    air = i.find('span', {'id': 'wob_dc'}).text.strip()
                    temp = i.find('span', {'id': 'wob_ttm'}).text.strip()
                    air_s = i.find_all('div', 'vk_gy vk_sh wob-dtl')
                    for k in air_s:
                        rain = k.find('span', {'id': 'wob_pp'}).text.strip()
                        wet = k.find('span', {'id': 'wob_hm'}).text.strip()
                        wind = k.find('span', 'wob_t').text.strip()
                embed = discord.Embed(
                    title=location + '의 날씨정보',
                    color=discord.Color.blue()
                )
                embed.add_field(name=loca_time,
                                value='현재온도: {}도 , {}\n강수확률: {}\n습도: {} 풍속: {}'.format(temp, air, rain, wet, wind))
                await app.send_message(message.channel, embed=embed)
                if int(temp) >= 30 and int(temp) <= 34:
                    await app.send_file(message.channel, fp='img_con/icon_49.png')
                elif int(temp) >= 35:
                    await app.send_file(message.channel, fp='img_con/icon_38.gif')
            except:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith('!영화'):
            sentence = message.content.split(' ')
            word = sentence[1]
            if word == '예정':
                embed = discord.Embed(
                    title='영화개봉예정',
                    color=discord.Color.dark_orange()
                )
                html = urllib.request.urlopen('https://movie.naver.com/movie/running/premovie.nhn')
                soup = BeautifulSoup(html, 'lxml')
                name = soup.find_all('dl', 'lst_dsc')
                for i in name:
                    c_name = i.find('a').text
                    c_kind = i.find('span', 'link_txt').text
                    c_kind = ''.join(c_kind.split())
                    embed.add_field(name='{}'.format(c_name), value='{}'.format(c_kind))
                await app.send_message(message.channel, embed=embed)

            if word == '상영중':
                embed = discord.Embed(
                    title='상영중인 영화',
                    color=discord.Color.dark_orange()
                )
                html = urllib.request.urlopen('https://movie.naver.com/movie/running/current.nhn')
                soup = BeautifulSoup(html, 'lxml')

                pre_order = soup.find_all('div', 'star_t1 b_star')
                title = soup.find_all('dt', 'tit')

                count = 1
                for i, k in zip(title, pre_order):
                    order_per = k.text.strip()
                    order_title = i.find('a').text
                    embed.add_field(name=str(count) + '번쨰', value='{}\n예매율: {}'.format(order_title, order_per))
                    count += 1
                    if count == 6:
                        break
                await app.send_message(message.channel, embed=embed)

        if message.content.startswith('!예매'):
            try:
                # str = '!예매 청주 목록'
                dt = datetime.datetime.now()
                today_time = dt.strftime('%Y%m%d')
                sentence = message.content.split(' ')
                user_loca = ''.join(sentence[1])
                user_word = ''.join(sentence[2:])
                data = {'title': [], 'link': []}
                df = pd.DataFrame(data)
                f = open('cgv_code.txt', 'r')

                embed = discord.Embed(
                    title=user_loca,
                    color=discord.Color.blue()
                )

                while True:
                    line = f.readline()
                    if not line:
                        break
                    re_line = line.split('//')
                    data['title'].append(re_line[0][3:])
                    data['link'].append(re_line[1][8:] + today_time)
                    df = pd.DataFrame(data)

                base_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx'
                cgv_url = 'http://www.cgv.co.kr'

                for q, w in zip(df['title'], df['link']):
                    if user_loca == q:
                        base_url = base_url + w

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

                html = requests.get(base_url, headers=headers).text
                soup = BeautifulSoup(html, 'lxml')
                stat = soup.find_all('div', 'col-times')

                cgv_data = {'movie': [], 'time': [], 'link': []}
                cgv_df = pd.DataFrame(cgv_data)

                for i in stat:
                    title = i.find('div').find('a').text.strip()
                    time_table = i.find_all('div', 'type-hall')
                    for k in time_table:
                        t_d = k.find('div', 'info-timetable').text.strip()
                        try:
                            link = k.find('div', 'info-timetable').find('a').get('href')
                        except AttributeError:
                            continue
                        cgv_data['movie'].append(title)
                        cgv_data['time'].append(t_d)
                        cgv_data['link'].append(link)
                        cgv_df = pd.DataFrame(cgv_data)

                if user_word == '목록':
                    count = 1
                    re_df = cgv_df.drop_duplicates(['movie'], keep='first')
                    for re_title, re_link in zip(re_df['movie'], re_df['link']):
                        d_link = '[%s](<%s>)' % (re_title, cgv_url + re_link)
                        embed.add_field(name=str(count) + '.', value='{}'.format(d_link))
                        count += 1
                    await app.send_message(message.channel, embed=embed)
                else:
                    await app.send_message(message.channel, 'command not found')
            except:
                await app.send_message(message.channel, 'command not found')


        if message.content.startswith('!환전'):
            try:
                sentence = message.content.split(' ')
                word = ''.join(sentence[1:])
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
                # h_word = urllib.parse.quote(word)
                url = 'https://www.google.co.kr/search?biw=531&bih=592&ei=YTQHXd7ZOJHm8wXhqrWQCA&q=' + word
                html = requests.get(url, headers=headers).text
                soup = BeautifulSoup(html, 'lxml')
                h_result = soup.find('div', 'dDoNo vk_bk gsrt')
                result = h_result.text.split(' ')
                await app.send_message(message.channel, result[0][:-3] + sentence[2])
            except:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith('!계산'):
            sentence = message.content.split(' ')
            word = ''.join(sentence[1:])
            n_word = urllib.parse.quote(word)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            url = 'https://www.google.com/search?q=' + n_word
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            n_result = soup.find('span', 'cwcot gsrt').text.strip()
            await app.send_message(message.channel, n_result)

        if message.content.startswith('!환율'):
            try:
                sentence = message.content.split(' ')
                user_input = sentence[1]
                p_word = urllib.parse.quote(user_input)
                embed = discord.Embed(
                    title='실시간 환율',
                    color=discord.Color.blue()
                )
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
                url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=' + p_word + '+환율'
                html = requests.get(url, headers=headers).text
                soup = BeautifulSoup(html, 'lxml')
                stat = soup.find_all('div', 'rate_tlt')
                for i in stat:
                    price = i.find('span', 'spt_con').text.strip().split(' ')
                    embed.add_field(name=user_input + '의 환율 정보',
                                    value='{}\n{} {}'.format(price[0][2:], price[2], price[3]))
                await app.send_message(message.channel, embed=embed)
            except:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith('!증시'):
            sentence = message.content.split(' ')
            n_word = ''.join(sentence[1:])

            h_url = 'https://www.wpws.kr/hangang/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            h_html = requests.get(h_url, headers=headers).text
            h_soup = BeautifulSoup(h_html, 'lxml')
            w_stat = h_soup.find('p', {'id': 'temp'}).text

            url = 'https://finance.naver.com/sise/'
            base_url = 'https://finance.naver.com'
            context = ssl._create_unverified_context()
            html = urlopen(url, context=context)
            soup = BeautifulSoup(html.read(), 'lxml')

            if n_word == '해외':
                embed = discord.Embed(
                    title='주요 해외 증시',
                    color=discord.Color.dark_orange()
                )
                url = 'http://finance-service.daum.net/global/index.daum'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
                html = requests.get(url, headers=headers).text
                soup = BeautifulSoup(html, 'lxml')
                stat = soup.select('#worldInfo')[0]
                i_title = stat.find_all('li')
                for i in i_title:
                    aa = re.sub('<.+?>', ' ', str(i)).strip().split('  ')
                    embed.add_field(name=aa[0], value='{}  {}  {}'.format(aa[1], aa[2], aa[3]))
                await app.send_message(message.channel, embed=embed)

            if n_word == '주요':
                embed = discord.Embed(
                    title='{}\n{}: {}'.format('주요 국내 증시', '현재 한강 수온', w_stat),
                    color=discord.Color.dark_orange()
                )

                k_stat = soup.find('div', 'lft')
                kos_price = k_stat.find_all('span', 'num')
                kos_stat = k_stat.find_all('span', 'num_s')
                kos = ['코스피', '코스닥', '코스피200']
                for a, b, c, in zip(kos_price, kos_stat, kos):
                    n_p = a.text
                    n_s = b.text
                    n_n = c
                    embed.add_field(name=n_n, value='{}\n{}'.format(n_p, n_s))
                await app.send_message(message.channel, embed=embed)

            if n_word == '유가':
                embed = discord.Embed(
                    title='국내외 유가',
                    color=discord.Color.dark_orange()
                )
                url = 'https://finance.naver.com/marketindex/?tabSel=gold#tab_section'
                context = ssl._create_unverified_context()
                html = urlopen(url, context=context)
                soup = BeautifulSoup(html.read(), 'lxml')
                stat = soup.find('table', 'tbl_exchange').find_all('tr')

                for i in stat:
                    try:
                        oil_name = i.find('a').text
                        price = i.find_all('td', 'num')
                        n, y, p = price
                        unit = i.find('td', 'unit').text
                        y_stat = i.find('img').get('alt')

                    except AttributeError:
                        continue
                    embed.add_field(name=oil_name,
                                    value='현재가: {}{}\n전일비: {} 등락율: {}\n{}'.format(n.text, unit, y.text, p.text, y_stat))
                await app.send_message(message.channel, embed=embed)

            if n_word == '인기':
                embed = discord.Embed(
                    title='인기 검색 종목',
                    color=discord.Color.dark_orange()
                )
                stat = soup.find('ul', 'lst_pop').find_all('li')
                count = 1
                for i in stat:
                    n_title = i.find('a').text
                    n_href = i.find('a').get('href')
                    price = i.find('span').text
                    link = base_url + n_href
                    title = '[%s](<%s>)' % (n_title, link)
                    embed.add_field(name=str(count) + '위', value='{}\n{}원'.format(title, price))
                    count += 1

                await app.send_message(message.channel, embed=embed)

        if message.content.startswith('!해축'):
            embed = discord.Embed(
                title='해축 정보',
                color=discord.Color.dark_orange()
            )
            sentence = message.content.split(' ')
            word = ''.join(sentence[1:])
            html = urllib.request.urlopen('https://sports.news.naver.com/wfootball/index.nhn')
            soup = BeautifulSoup(html, 'lxml')
            base_url = 'https://sports.news.naver.com'

            if word == '주요':
                s_count = 1
                stat = soup.find('div', 'home_news').find_all('li')
                for i in stat:
                    title = i.find('a').text.strip()
                    link = i.find('a').get('href')
                    i_s_n = '[%s](<%s>)' % (title, base_url + link)
                    embed.add_field(name=str(s_count) + '.', value='{}'.format(i_s_n))
                    s_count += 1
                await app.send_message(message.channel, embed=embed)
            else:
                await app.send_message(message.channel, 'command not found')

        if message.content.startswith('!남대문'):
            embed = discord.Embed(
                title='위스키 판매 목록',
                color=discord.Color.red()
            )
            sentence = message.content.split(' ')
            w_name = ''.join(sentence[1:])
            df = pd.read_csv('new_namdeon_list.csv')
            for a, b, c, d, e, k, q in zip(df['title'], df['price'], df['year'], df['cask'], df['seller'], df['date'],
                                           df['ml']):
                try:
                    if w_name in a:
                        embed.add_field(name='{} {}({})\n{}원'.format(a, c, d, int(float(b))),
                                        value='{} {} {}'.format(e, q, k))
                except:
                    continue
            await app.send_message(message.channel, embed=embed)

            # w_dict= {}
            # for i in sheet1.iter_rows(min_row=3):
            #     title = i[1].value
            #     price = i[4].value
            #     w_dict[title]=price

        if message.content.startswith('!스팀'):
            embed = discord.Embed(
                title='스팀 특별할인 목록',
                color=discord.Color.green()
            )
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
            url = 'https://store.steampowered.com/search/?specials=1&os=win'
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            stat = soup.find_all('div', 'responsive_search_name_combined')
            game_page = soup.find('div', {'id': 'search_results'})
            game_stat = game_page.find('div', {'id': 'search_result_container'})
            link = game_stat.find_all('a')
            count = 1
            for i, k in zip(stat, link):
                try:
                    title = i.find('div', 'col search_name ellipsis').text.strip()
                    price = i.find('div', 'col search_price discounted responsive_secondrow').text.strip().split('$')
                    per = i.find('div', 'col search_discount responsive_secondrow').text.strip()
                    g_link = k.get('href')
                    url = '[%s](<%s>)' % (title, g_link)
                except AttributeError:
                    continue
                embed.add_field(name=str(count) + '.',
                                value=url + '\n''정가:{} , 할인가:{}\n할인률:{}'.format('~~' + '$' + price[1] + '~~',
                                '$' + price[2], per))
                count += 1
            await app.send_message(message.channel, embed=embed)

    token = '1234567890'
    # personal_token_value
    app.run(token)


if __name__ == '__main__':
    main()
