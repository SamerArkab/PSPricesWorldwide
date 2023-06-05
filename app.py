# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:32:55 2022

@author: samra
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import requests
from bs4 import BeautifulSoup


# Dictionary of 10 countries
countries = {
    "Brasil": "pt-br",
    "India": "en-in",
    "Israel": "en-il",
    "Italy": "it-it",
    "Romania": "en-ro",
    "Spain": "es-es",
    "Sweden": "en-se",
    "Thailand": "en-th",
    "Turkey": "en-tr",
    "United States": "en-us"
}

app = Flask(__name__)

cors = CORS(app)

@app.route('/app/search')
def search():
    # Retrieve game name from query parameter
    game = request.args.get('game')
    print("Searching for the cheapest prices for " + game + " has begun.")
    if not game:
        return jsonify({'error': 'No game name provided'}), 400

    # Initialize for building the DataFrame object
    prices_lst = []
    names_lst = []
    desc_txt = ""
    game_poster = ""

    # Initialize ps store root link
    ps_store = "https://store.playstation.com"

    # Search for the desired game
    to_search = game

    # Retrieve URL of the game's link for all countries and information about prices (or discount price - if exists)
    # Also retrieve the game's poster link and description, only from the Israeli store
    for country in countries.values():
        # Prepare URL to search for the game
        URL = ps_store + "/" + country + "/search/" + to_search
        print("Now checking the prices in " + list(countries.keys())[list(countries.values()).index(country)])

        # Retrieve the html file of the results using lxml parser, which provides an API for parsing XML and HTML files
        source = requests.get(URL).text
        soup = BeautifulSoup(source, 'lxml')

        try:
            # Find the link for the game's page
            game_link = soup.find("a", {"class": "psw-link psw-content-link"})
            game_link_index = str(game_link).index("href=") + 13  # Starting index of game's link
            game_link_end_index = str(game_link).index(" id=") - 1
            game_link_url = str(game_link)[game_link_index:game_link_end_index]
            # print(game_link_url)

            # Get the game's poster link + description from the Israeli store
            if country == "en-il":
                game_poster_container = soup.find("span", {"class": "psw-media-frame psw-fill-x psw-image psw-media "
                                                                    "psw-media-interactive psw-aspect-1-1"})
                game_poster_img_container = game_poster_container.noscript.img
                poster_src_index = str(game_poster_img_container).index("src=") + 5  # Starting index of poster URL
                game_poster = str(game_poster_img_container)[poster_src_index:-3]  # Save game's poster URL
                # print(game_poster)

            # Create full URL for the game's specific page
            found_url = ps_store + "/" + country + "/" + game_link_url
            # print(found_url)

            # Request the HTML file
            game_source = requests.get(found_url).text
            game_soup = BeautifulSoup(game_source, 'lxml')

            # Retrieve game's full name and append it to the names list
            game_name = game_soup.find("h1", {"data-qa": "mfe-game-title#name"})
            name_index = str(game_name).index("#name") + 7
            name_end_index = -5
            name_str = str(game_name)[name_index:name_end_index]
            names_lst.append(name_str)

            # Get game description from the Israeli store
            if country == "en-il":
                get_description = game_soup.find("p", {"data-qa": "mfe-game-overview#description"})
                desc_index = str(get_description).index("#description") + 14
                desc_end_index = -4
                desc_txt = str(get_description)[desc_index:desc_end_index]
                desc_txt = desc_txt.replace("<br/>", "\n")  # Replace HTML's break row to string's new line

            get_price = game_soup.find("span", {"data-qa": "mfeCtaMain#offer0#finalPrice"})
            # print(get_price)
            price_index = str(get_price).index("finalPrice") + 12  # Starting index of game price
            price_end_index = -7
            contain_num = False  # Initialize with each loop
            for i in str(get_price)[price_index:price_end_index]:
                if i.isdigit():  # Check if game price data contains a number
                    contain_num = True

            if contain_num:
                prices_lst.append(str(get_price)[price_index:price_end_index])
            else:  # If it doesn't contain a number, this means the game's offered for free
                prices_lst.append("Free")

        except:  # Game is not available in the following country's store
            print("Game is not available in " + list(countries.keys())[list(countries.values()).index(country)])
            prices_lst.append("Not available")
            names_lst.append("Not available")
    # print(prices_lst)

    # Create DataFrame object with the game's name and price (or discount price) for each country
    game_prices = pd.DataFrame({"Country": list(countries.keys()), "Name": names_lst, "Price": prices_lst})

    # Set up response dictionary
    response = {
        "game": game,
        "prices": game_prices.to_dict('records'),
        "description": desc_txt,
        "poster": game_poster
    }

    # Return response in JSON format
    print("API's work is over.\nReturning the response.")
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)

'''
df = pd.DataFrame()
df.insert(0, "Name", names_lst)
df.insert(1, "Country", list(countries.keys()))
df.insert(2, "Price", prices_lst)
df.insert(3, "Game Description", "")
df.insert(4, "Game's poster link", "")

df.at[21, "Game's poster link"] = game_poster
df.at[22, "Game Description"] = desc_txt

# DataFrame object doesn't recognize some signs with the default encoding, so use the following:
df.index = df.index + 1
df.to_csv("prices.csv", encoding="utf-8-sig")
print(df)
'''