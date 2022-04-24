from bs4 import BeautifulSoup
import requests


def main2(player_search):
    webscraped_list = webscrape(player_search)
    if not webscraped_list:
        return None
    search_result = search(player_search, webscraped_list)

    if search_result is not False:
        cleanid_result_sorted = id_cleaner(search_result)
        id_sorted_list = id_sorter(cleanid_result_sorted)

        player_sorted_list = player_sort(id_sorted_list)
        elo_sorted_list = sort_by_elo(player_sorted_list)
        return elo_sorted_list
    else:
        return None


def webscrape(player_search):
    value_list = []
    new_list = []
    source = requests.get(f'http://ratingupdate.info/?name={player_search}').text
    soup = BeautifulSoup(source, 'lxml')

    for x in soup.find('div', class_='table-container').find_all('td'):
        player_data = x.text
        if "→" in player_data:
            player_data = player_data.replace(" →\n", "")
            test = x.find('a', href=True)
            player_id = test["href"]
            value_list.append(player_id)
        value_list.append(player_data)
        new_list = [value_list[i:i + 5] for i in range(0, len(value_list), 5)]

    return new_list


def search(user_search, webscraped_list):
    newer_list = []
    for i, z in enumerate(webscraped_list):  # i dont think enumerate is needed?
        if user_search.lower() == z[1].lower():
            newer_list.append(z)
    return newer_list


def id_cleaner(search_result):
    cleanid_result = []
    for z in search_result:
        temp_id = z[0]
        temp_id = temp_id[:-3]
        temp_id = temp_id.replace("/player/", "")
        cleanid_result.append(temp_id)
        for i, elements in enumerate(z):
            if elements == z[0]:
                continue
            cleanid_result.append(z[i])
    cleanid_result_sorted = [cleanid_result[i:i + 5] for i in range(0, len(cleanid_result), 5)]
    return cleanid_result_sorted


def id_sorter(clean_id):
    temp_id_sort = []
    perm_id_sort = []
    for ix, elems in enumerate(clean_id):
        if ix == 0:
            temp_id_sort.append(elems)
            perm_id_sort.append(elems)
            continue
        new_player_id = elems[0]

        for zx, ex in enumerate(temp_id_sort):
            old_player_id = ex[0]
            if new_player_id == old_player_id:
                temp_id_sort.insert(zx, elems)
                perm_id_sort.insert(zx, elems)
                break
            elif new_player_id != old_player_id:
                if new_player_id != old_player_id and ex == temp_id_sort[-1]:
                    temp_id_sort.insert(zx + 1, elems)
                    break
                else:
                    continue

# I need to loop over this: cleanid_result_sorted = [cleanid_result[i:i + 5] for i in range(0, len(cleanid_result), 5)]
    temp_id_sort.reverse()
    return temp_id_sort


def player_sort(id_sorted_list):
    temp_player_sort = []
    new_player_list = []
    for ix, elems in enumerate(id_sorted_list):
        if ix == 0:
            temp_player_sort.append(elems)
            continue

        if elems[0] == id_sorted_list[ix-1][0]:
            temp_player_sort.append(elems)

        elif elems[0] != id_sorted_list[ix-1][0]:
            testo = temp_player_sort.copy()
            new_player_list.append(testo)
            temp_player_sort.clear()
            temp_player_sort.append(elems)
    temp_2 = temp_player_sort.copy()
    new_player_list.append(temp_2)
    return new_player_list


def sort_by_elo(player_sorted_list):
    perm_elo_sort = []
    temp_elo_sort = []
    for lists in player_sorted_list:
        if temp_elo_sort:
            testo = temp_elo_sort.copy()
            testo.reverse()
            perm_elo_sort.append(testo)
            temp_elo_sort.clear()
        for ix, elems in enumerate(lists):
            if ix == 0:
                temp_elo_sort.append(elems)
                continue
            just_elo = elo_splitter(elems[3])

            for zx, ex in enumerate(temp_elo_sort):
                ex_elo = elo_splitter(ex[3])
                if just_elo > ex_elo:
                    temp_elo_sort.insert(zx, elems)
                    break
                elif just_elo < ex_elo:
                    if just_elo < ex_elo and ex == temp_elo_sort[-1]:
                        temp_elo_sort.insert(zx + 1, elems)
                        break
                    else:
                        continue
                elif just_elo == ex_elo:
                    temp_elo_sort.insert(zx, elems)
                    break
                else:
                    temp_elo_sort.insert(zx, elems)
                    break
    testo = temp_elo_sort.copy()
    testo.reverse()
    perm_elo_sort.append(testo)
    temp_elo_sort.clear()
    return perm_elo_sort


def elo_splitter(unsplit_elo):
    just_elo = unsplit_elo
    just_elo = just_elo.split(" ±")  # splits the elo string into a list
    just_elo = just_elo[0]  # gives me only the elo number in the list
    just_elo = int(just_elo)
    return just_elo


def paste(search_data):
    perm_string = ""
    temp_string = ""
    max_chr_alert = False
    length_check = 0
    for elements in search_data:
        if length_check > 1024:
            max_chr_alert = True
            break
        if perm_string:
            new_player = "__***New player below!***__\n"
            perm_string = new_player + perm_string
        for ele in elements:
            length_check = len(temp_string + perm_string)
            if length_check > 1024:
                max_chr_alert = True
                break
            temp_string = f"**{ele[1]} **| *{ele[2]}* | {ele[3]} | {ele[4]}\n"
            perm_string = temp_string + perm_string
    return perm_string, max_chr_alert
