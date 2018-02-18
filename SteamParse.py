from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import csv

filename = "games.csv"

f = open(filename, "w", encoding='utf-8')

headers = "name, discount, original_price, new_price, savings\n"

f.write(headers)

print("Processing...")

for i in range(10):
    steamURL = 'http://store.steampowered.com/search/?specials=1&page={}'.format(i + 1)

    sClient = urlopen(steamURL)

    steam_html = sClient.read()

    sClient.close()

    steam_soup = soup(steam_html, "html.parser")

    game_deals = steam_soup.findAll("div", {"class": "responsive_search_name_combined"})

    for game_deal in game_deals:
        name = game_deal.find("span", {"class": "title"}).text.strip()

        discount = game_deal.find("div", {"class": "col search_discount responsive_secondrow"}).text.strip()

        price_raw = game_deal.find("div", {"class": "col search_price discounted responsive_secondrow"}).text.strip().split('$')
        print(price_raw)

        try:
            price_old = "${:.2f}".format(float(price_raw[1]))
            price_new = "${:.2f}".format(float(price_raw[2]))
            savings_raw = float(price_raw[1]) - float(price_raw[2])
            savings = "${:.2f}".format(savings_raw)
            print(discount)
        except ValueError:
            pass

        f.write(name.replace(",", "|") + "," + discount + "," + price_old + "," + price_new + "," + savings + "\n")

print("Success!")

f.close()
