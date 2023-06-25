from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
from .models import RaceInfo
from .models import RaceResult
import datetime
from django.db import transaction
import re


# Create your views here.
class ScrapingView(TemplateView):
    template_name = "scraping.html"

    def get(self, request):
        updated_date = RaceInfo.objects.order_by('race_date').values('race_date').last()

        if updated_date is None:
            params = {"updated_date": 'not update'}
        else:
            params = {"updated_date": "updated by " + str(updated_date['race_date'])}
        return render(request, self.template_name, params)

    def post(self, request):
        updated_date = main()
        params = {"updated_date": "updated by " + str(updated_date['race_date'])}
        return render(request, self.template_name, params)


# 現在時刻からDBをupdateする
def main():
    updated_date = RaceInfo.objects.order_by('race_date').values('race_date').last()
    if updated_date is None:
        start_date = datetime.date(2018, 1, 1)
    else:
        start_date = updated_date['race_date'] + datetime.timedelta(days=1)  # 開始日を指定

    end_date = datetime.date.today()  # 今日の日付を取得

    current_date = start_date
    while current_date <= end_date:

        # レースが開催された日にちをfor分で回す
        for date in get_race_date(current_date.year, current_date.month):
            if datetime.datetime.strptime(date, '%Y%m%d').date() >= start_date:
                db_update(date)

        next_month = current_date.month + 1
        next_year = current_date.year
        if next_month > 12:
            next_month = 1
            next_year += 1

        current_date = current_date.replace(month=next_month, year=next_year, day=1)

    updated_date = RaceInfo.objects.values('race_date').last()

    return updated_date


def db_update(date):
    with transaction.atomic():

        # 日にちからレースIDを取得
        for race_id in get_race_id(date):

            # レースIDからレース情報を取得
            pre_race_info = get_race_info(race_id)
            if pre_race_info is not None:
                race_info = pre_race_info[0]
            else:
                continue

            # レース情報をDBにCreate
            RaceInfo.objects.create(
                race_id=race_id,
                race_date=datetime.datetime.strptime(race_info["日付"][0], '%Y/%m/%d').date(),
                start_time=datetime.datetime.strptime(race_info["発走時刻"][0], '%H:%M').time(),
                distance=int(race_info["距離(m)"][0]),
                direction=race_info["方向"][0],
                ground_type=race_info["地面種類"][0],
                ground_condition=race_info["地面状態"][0],
                weather=race_info["天候"][0],
                race_cource=race_info["競馬場"][0],
                entries=int(race_info["頭数"][0]),
            )

            # レースIDからレース結果を取得
            race_results = get_race_info(race_id)[1]

            for index in race_results.T:
                # レース結果をDBにCreate
                RaceResult.objects.create(
                    race_id=race_id,
                    horse_id=race_results["馬ID"][index],
                    horse_name=race_results["馬名"][index],
                    order=race_results["着 順"][index],
                    bracket_number=race_results["枠 番"][index],
                    sexual_age=race_results["性齢"][index],
                    weight=race_results["斤量"][index],
                    time=race_results["タイム"][index],
                    horse_weight=race_results["馬体重"][index],
                )
    return


# 対象年度、月からレースが開催された日にち(文字列)を返す
def get_race_date(year, month):
    # レースを開催した日を抽出したい年月を指定
    url = f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"

    # レース開催日のデータを取得
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    calender = soup.find_all(class_="RaceKaisaiBox HaveData")

    # 数字の抽出準備
    number = re.compile("\d+")

    # 開催日の文字列をyyyymmddで作成
    hold_day_list = number.findall(str(calender))
    hold_date = []
    for hold_day in hold_day_list:
        hold_date.append(str(year) + '{:02}{:02}'.format(month, int(hold_day)))

    return hold_date


# レースの日時から開催されたレースIDを返す
def get_race_id(date):
    # 日付を指定
    url = f"https://race.netkeiba.com/top/race_list.html?kaisai_date={date}"

    # chrome driver
    driver = webdriver.Chrome(r"C:\Users\81704\Desktop\appdiv\test\chromedriver_win32\chromedriver")

    # 取得先URLにアクセス
    driver.get(url)
    # コンテンツが描画されるまで待機
    time.sleep(5)
    # 抽出
    elements = driver.find_elements(By.XPATH, "//a[@href]")
    # urlだけを抽出
    url_list = []
    for element in elements:
        url_list.append(element.get_attribute('href'))

    # プラウザを閉じる
    driver.quit()

    # レース映像のurlを取得
    url_movie_list = []
    for a_url in url_list:
        if "movie" in a_url:
            url_movie_list.append(a_url)

    # レース映像のurlからレースIDを取得
    race_id_list = []
    number = re.compile("\d+")
    for url_movie in url_movie_list:
        race_id_list.append(number.findall(url_movie)[0])

    return race_id_list


# レースIDからレース情報を取得
def get_race_info(race_id):
    # 文字列の中からリストに該当する単語を抽出
    def extract_info(some_list, some_string):
        correct = "error"
        for some_data in some_list:
            if some_data in str(some_string):
                correct = some_data
        return correct

    # 特定の文字の直前の数字を取得
    def get_number_before_character(string, character):
        pattern = r"(\d+)" + re.escape(character)
        match = re.search(pattern, string)
        if match:
            return int(match.group(1))
        else:
            return '00'

    # 特定の文字の直後の数字を取得
    def get_number_after_character(string, character):
        pattern = re.escape(character) + r"(\d+)"
        match = re.search(pattern, string)
        if match:
            return int(match.group(1))
        else:
            return '00'

    # raceIDを指定
    url = "https://db.netkeiba.com/"
    url_race = url + "race/" + race_id + "/"

    # レース結果テーブルの作成
    # レース結果の表を取得
    table_result = pd.read_html(url_race, header=0)

    # 馬IDを取得
    r = requests.get(url_race)
    soup = BeautifulSoup(r.content, "html.parser")
    horse_id_raw = soup.find_all(class_="txt_l")

    # horseID_rawから馬IDのみを抽出
    horse_id = []
    for i in range(len(horse_id_raw)):
        if i % 4 == 0:
            num_list1 = re.findall(r"\d+", str(horse_id_raw[i]))
            horse_id.append(num_list1[0])
            # print(horseID)

    # KeyErrorの場合は、該当レースが中止なのでスキップ
    try:
        # 馬IDをレース結果テーブルに追加
        table_result[0]["馬ID"] = horse_id
        table_race_result = table_result[0]

    except IndexError:
        return None

    # レース情報テーブルの作成
    # 抽出に必要なリストの作成
    ground_list = ["芝", "ダート"]
    condition_list = ["良", "稍重", "重"]
    weather_list = ["曇", "小雨", "晴", "雨", "雪"]
    direction_list = ["右", "左", "障", "直線"]
    place_list = ["中京", "東京", "阪神", "中山", "福島", "小倉", "新潟", "京都", "札幌", "函館"]

    # 情報１の取得
    data_infomation1 = soup.find_all("span", text=re.compile("天候"))
    # 情報2の取得
    data_infomation2 = soup.find_all("p", class_="smalltxt")

    # 距離を抽出
    length = get_number_before_character(str(data_infomation1), 'm')

    # 発走時を抽出
    start_hour = get_number_before_character(str(data_infomation1), ':')

    # 発走分を取得
    start_minutes = get_number_after_character(str(data_infomation1), ':')

    # 日付を抽出
    matches = re.findall(r"\d{4}年\d{1,2}月\d{1,2}日", data_infomation2[0].text)

    # 日付文字列をdate型に変換
    try:
        date = matches[0].replace("年", "/").replace("月", "/").replace("日", "")
    except:
        date = '2000/01/01'

    table_race_infomation = pd.DataFrame({"日付": date,
                                          "発走時刻": f"{start_hour}:{start_minutes}",
                                          "距離(m)": length,
                                          "方向": extract_info(direction_list, data_infomation1),
                                          "地面種類": extract_info(ground_list, data_infomation1),
                                          "地面状態": extract_info(condition_list, data_infomation1),
                                          "天候": extract_info(weather_list, data_infomation1),
                                          "競馬場": extract_info(place_list, data_infomation2),
                                          "頭数": len(horse_id)},
                                         index=[str(race_id)])

    return table_race_infomation, table_race_result


# 馬IDかた馬情報を取得
def get_horse_info(horse_id):
    # 文字列の中からリストに該当する単語を抽出
    def extract_info(some_list, some_string):
        for some_data in some_list:
            if some_data in str(some_string):
                correct = some_data
        return correct

    # raceIDを指定
    url = "https://db.netkeiba.com/"
    url_horse = url + "horse/" + horse_id + "/"

    # 馬データの文字列を取得
    r = requests.get(url_horse)
    soup = BeautifulSoup(r.content, "html.parser")
    horsedata_raw1 = soup.find_all("h1")
    horsedata_raw2 = soup.find_all(class_="txt_01")

    # 抽出単語のリスト
    om_list = ["牝", "牡"]
    state_list = ["現役", "抹消"]

    # 数字とカタカナの抽出準備
    katakana = re.compile("[\u30A1-\u30FF]+")
    number = re.compile("\d+")

    table_horse_infomation = pd.DataFrame({"馬ID": horse_id,
                                           "馬名": katakana.findall(str(horsedata_raw1[1])),
                                           "性別": extract_info(om_list, horsedata_raw2),
                                           "年齢": number.findall(str(horsedata_raw2))[1],
                                           "状態": extract_info(state_list, horsedata_raw2)}, )
    return table_horse_infomation
