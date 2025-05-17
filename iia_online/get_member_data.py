import pandas as pd
import requests

from iia_online.urls import CHAPTER_LIST, CHAPTER_LIST_CONDITION, CATEGORY_LIST, GET_MEMBER_LIST


def get_chapter_list():
    params = {"Param": "t"}
    response = requests.post(CHAPTER_LIST, json=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df.to_excel("chapter_list.xlsx")




def get_chapter_list_condition():
    params = {}
    response = requests.post(CHAPTER_LIST_CONDITION, json=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df.to_excel("chapter_list_condition.xlsx")


def get_category():
    params = {}
    response = requests.post(CATEGORY_LIST, json=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df.to_excel("category.xlsx")

def get_member_list(chapter, status, cate, unit, product, memberid):
    params = {"chapter": chapter, "status": status, "cate": cate, "unit": unit, "product": product,
              "memberid": memberid}
    response = requests.post(GET_MEMBER_LIST, json=params)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    df = df.drop('password', axis=1)
    df.to_excel("member_list.xlsx")



get_member_list('', '1', '', '', '', '')
