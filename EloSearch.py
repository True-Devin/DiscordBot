from bs4 import BeautifulSoup
import requests


def main(character, player_search):
    value_list = []
    character_search = character.upper()[0:2]
    source = requests.get(f'http://ratingupdate.info/top/{character_search}').text
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
