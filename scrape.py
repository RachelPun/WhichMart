# ========== IMPORTS ==========
import re
import requests
from bs4 import BeautifulSoup


# ========== SCRAPER: TESCO ==========
class Tesco:
    """Tesco scraper"""

    def __init__(self, headers, search):
        self.base_url = "https://www.tesco.com/groceries/en-GB"
        self.headers = headers
        self.search = search

    @property
    def search_url(self) -> str:
        """Returns initial search URL."""
        return self.base_url + f"/search?query={'%20'.join(self.search.split())}"

    @property
    def categories(self) -> dict:
        """Return a list of available categories for given search results."""

        response = requests.get(self.search_url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")

        categories = soup.find("li", attrs={"data-auto": "filter-categories"}
                               ).find("div", class_="filter-options"
                                      )
        categories = categories.find_all(
            "li", class_="filter-option__container")

        results = {}
        for category in categories:
            option = category.get("id")
            link = category.find("a", class_="filter-option--link").get("href")
            results[option] = link

        return results.keys()

    @property
    def last_page(self) -> int:
        """Returns the amount of pages of search results."""

        response = requests.get(self.search_url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        last_page_number = soup.find("a",
                                     class_=re.compile(
                                         "pagination--button prev-next.*"),
                                     title="Go to results page"
                                     ).find_parent("li").find_previous_sibling().find("span").text

        return int(last_page_number)

    def scrape_all_items(self) -> list[tuple]:
        """Returns all searched and filtered items' information."""

        if self.last_page > 1:
            pages = [self.search_url+f"&page={num}"
                     for num in range(2, self.last_page+1)]
        else:
            pages = []

        products = []
        for page in [self.search_url] + pages:

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
                    products.append((product, price))

        return products


# ========== MAIN ==========
if __name__ == "__main__":

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"}

    apple_1 = "https://www.tesco.com/groceries/en-GB/search?query=apples&department=Fresh%20Fruit&viewAll=department"
    tesco_1 = "https://www.tesco.com/groceries/en-GB/search?query=tesco"  # 241->239
    pack_1 = "https://www.tesco.com/groceries/en-GB/search?query=pack"  # 89
    G500_1 = "https://www.tesco.com/groceries/en-GB/search?query=500G"  # 21
    mattress_1 = "https://www.tesco.com/groceries/en-GB/search?query=mattress"  # 1

    tesco = Tesco(headers, "apple")
    tesco.categories
    # print(tesco.scrape_all_items())
