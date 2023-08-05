# coding:utf-8

import requests
import time
import re
import os
import urllib
import json
import sys


def get_realtime(stock_no):

    GET_STOCK_NO_URL = "http://mis.twse.com.tw/stock/api/getStock.jsp?ch=" + \
        str(stock_no) + ".tw&json=1"

    res = requests.get(GET_STOCK_NO_URL)
    data = res.json()

    if data["rtcode"] == "0000" and len(data["msgArray"]) > 0 and 'key'in data["msgArray"][0]:
        GET_STOCK_INFO = "http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=" + \
            data["msgArray"][0]["key"] + "&json=1&delay=0"

        res = requests.get(GET_STOCK_INFO)
        data = res.json()
        if 'z' in data["msgArray"][0] and 'h' in data["msgArray"][0] and 'l' in data["msgArray"][0]:
            return json.dumps({
                "stock_no": stock_no,
                "now_price": data["msgArray"][0]["z"],
                "high_price": data["msgArray"][0]["h"],
                "low_price": data["msgArray"][0]["l"]
            })
        else:
            return json.dumps({
                "stock_no": stock_no,
                "now_price": "-1",
                "high_price": "-1",
                "low_price": "-1"
            })
    else:
        return json.dumps({
            "stock_no": stock_no,
            "now_price": "-1",
            "high_price": "-1",
            "low_price": "-1"
        })
