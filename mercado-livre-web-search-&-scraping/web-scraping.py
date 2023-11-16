import logging
import os
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from datetime import datetime
import ssl
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context

search = ["ar-condicionado"]

pages = []
data = []
now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def getting_products_details():
    for s in search:
        req = Request(url= f"https://lista.mercadolivre.com.br/{s}", headers={"User-Agent": "Mozilla/5.0"})
        html_doc = urlopen(req).read()    
        soup = BeautifulSoup(html_doc, "html.parser")

        pageQty = soup.find("li", class_="andes-pagination__page-count").text.strip()
        pageQty = int(pageQty.split(" ")[-1])
        searchLink = soup.find("li", class_="andes-pagination__button andes-pagination__button--next").find("a").get("href")

        pages.append(f"https://lista.mercadolivre.com.br/{s}")
        aux_var = 0
        for i in range(pageQty):
            pages.append(searchLink.replace("51", str(51+aux_var)))
            aux_var += 50

    # Getting_products_details
    for link in pages:
        req = Request(url = link, headers={"User-Agent": "Mozilla/5.0"})
        html_doc = urlopen(req).read()    
        search_page_soup = BeautifulSoup(html_doc, "html.parser")

        for item in search_page_soup.find_all("li", class_ = "ui-search-layout__item"):

            productTitle = item.find("a").get("title")
            productLink = item.find("a").get("href")
            productPrice = item.find("span", class_="andes-money-amount").text.strip()
            productRatings = "" if (item.find("span", class_="ui-search-reviews__rating-number")) is None else (item.find("span", class_="ui-search-reviews__rating-number").text.strip())

            data.append({"searchedCategory": s
                    ,"productTitle": productTitle
                    ,"productLink": productLink
                    ,"productPrice": productPrice
                    ,"productRatings": productRatings
                    ,"insertDate": now
            })

    return data

def write_csv(data, filepath='/home/dfinotti/web-scraping-trainning/mercado-livre-web-search-&-scraping/csv/'):

    filename = 'products_scraping'+ datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.csv'
    filepath = filepath+filename 
    keys = data[0].keys()
    with open( filepath, 'w+', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

getting_products_details()
write_csv(data)