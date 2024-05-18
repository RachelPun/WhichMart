import re
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"}

    response = requests.get(
        "https://www.tesco.com/groceries/en-GB/search?query=apples&department=Fresh%20Fruit&viewAll=department",
        headers=headers)

    soup = BeautifulSoup(response.text, features="html.parser")

    divs = soup.find("div", class_="product-lists")
    current = divs.find(
        "div", class_="search product-list--page product-list--current-page")
    for wrapper in current.find_all("div", class_="product-details--wrapper"):
        price_box = wrapper.find(
            "div", class_=re.compile(r"base-components__RootElement.*price__container"))
        if price_box:
            price = price_box.find(
                "p", class_=re.compile(r"styled__StyledHeading.*price__text.*")).text
            product = wrapper.find(
                "span", class_=re.compile(r"styled__Text.*link__text")).text
            print(product, price)
