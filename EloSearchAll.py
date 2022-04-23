from bs4 import BeautifulSoup
import requests

# Loop through all the characters to obtain every single person in the top 100 list at the start of elo upda-
# te maybe cause if I do it in every bot command it might be too many requests i.e. accidental ddos
# Create a list for each character and their top 100 players' data
# User should be able to input character and player to get the elo for that players' character
# (I am not sure What I should do with usernames that are the same)


def main(player_search):
    value_list = []
    character_list = ["so", "ky", "ma", "ax", "ch", "po", "fa", "mi", "za", "ra",
                      "le", "na", "gi", "an", "in", "go", "ja", "ha", "ba", "te"]

    for champ in character_list:
        source = requests.get(f'http://ratingupdate.info/top/{champ}').text
        soup = BeautifulSoup(source, 'lxml')

        for x in soup.find('div', class_='table-container').find_all('td'):
            player_data = x.text
            if "→" in player_data:
                player_data = player_data.replace(" →\n", "")
            value_list.append(player_data)
            new_list = [value_list[i:i + 4] for i in range(0, len(value_list), 4)]

        search_result = search(player_search, new_list)

        if search_result is not False:
            # result = f"Rank: #{search_result[0]} | Name: {search_result[1]} | Elo: {search_result[2]} "
            return search_result
        else:
            # result = "Player not found"
            return None


def search(user_search, new_list):
    for z in new_list:
        if user_search.lower() == z[1].lower():
            return z
    return False
