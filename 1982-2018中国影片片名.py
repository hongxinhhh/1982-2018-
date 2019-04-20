# -*-coding:utf-8-*-
import requests
import csv
from bs4 import BeautifulSoup
import json
import os
import time

CSV_FILE_NAME = "1982-2018中国影片.csv"
CSV_TITLE = ["年份", "影片名"]


def main():
    """
    程序主函数
    :return:
    """
    global CSV_FILE_NAME, CSV_TITLE
    # 创建csv文件
    create_csv(CSV_FILE_NAME, CSV_TITLE)
    for year in range(1982, 2019):
        # 采集完数据存放到st_data中并写入csv
        # 中国大陆的编号是“50”
        lst_data = get_movie_names(year, "50")
        time.sleep(1)
        save_csv(CSV_FILE_NAME, lst_data)
    print("程序处理完毕")


def get_movie_names(year, area):
    """
    根据地区和年份采集影片名称
    :param year:
    :param area:
    :return:
    """
    if not year or not area:
        return
    print(year, area)
    lst_all_data = []
    url = "http://www.cbooo.cn/Mdata/getMdata_movie?area=%s&year=%d&initial=全部&pIndex=1" % (area, year)
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    })
    response.encoding = "utf-8"
    text = response.text
    datas_json = json.loads(text)
    # 获取总页数
    total_page = datas_json.get("tPage")
    # 获取第一页的数据
    lst_data = datas_json.get("pData")
    # 将第一页数据加入到lst_all_data中
    if lst_data:
        lst_all_data += lst_data
    # 从第二页开始抓取到总页数
    page = 2
    while page <= total_page:
        url = "http://www.cbooo.cn/Mdata/getMdata_movie?area=%s&year=%d&initial=全部&pIndex=%d" % (area, year, page)
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        })
        response.encoding = "utf-8"
        text = response.text
        datas_json = json.loads(text)
        lst_data = datas_json.get("pData")
        if lst_data:
            lst_all_data += lst_data
        page += 1
    lst_result = []
    # 采集完数据后，将年份和影片名称写入列表，并追加到lst_result里面
    for data in lst_all_data:
        result = [""] * len(CSV_TITLE)
        result[0] = year
        if data.get("MovieName"):
            result[1] = data.get("MovieName")
        print(result)
        lst_result.append(result)
    # 最终返回这个lst_result
    return lst_result


def create_csv(file_name, title):
    """
    创建csv文件
    :return:
    """
    if os.path.exists(file_name):
        return
    with open(file_name, "w", encoding="utf-8", newline="") as file:
        csv_write = csv.writer(file)
        csv_write.writerow(title)


def save_csv(file_name, lst_data):
    """
    保存数据
    :param file_name:
    :param lst_data:
    :return:
    """
    if not file_name or not lst_data:
        return
    with open(file_name, "a", encoding="utf-8", newline="") as file:
        csv_write = csv.writer(file)
        for data in lst_data:
            csv_write.writerow(data)


# 程序入口
if __name__ == '__main__':
    main()
