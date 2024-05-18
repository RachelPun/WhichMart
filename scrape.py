import re
import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"}

    apple_1 = "https://www.tesco.com/groceries/en-GB/search?query=apples&department=Fresh%20Fruit&viewAll=department"
    tesco_1 = "https://www.tesco.com/groceries/en-GB/search?query=tesco"  # 241->239
    pack_1 = "https://www.tesco.com/groceries/en-GB/search?query=pack"  # 89
    G500_1 = "https://www.tesco.com/groceries/en-GB/search?query=500G"  # 21
    mattress_1 = "https://www.tesco.com/groceries/en-GB/search?query=mattress"

    response = requests.get(apple_1, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    last_page = int(soup.find("a", class_=re.compile("pagination--button prev-next.*"), title="Go to results page"
                              ).find_parent("li").find_previous_sibling().find("span").text)

    for page in [apple_1] + [apple_1+f"&page={num}" for num in range(2, last_page+1)]:

        response = requests.get(page, headers=headers)
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
