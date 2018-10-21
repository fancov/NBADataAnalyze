import requests
from bs4 import BeautifulSoup
import csv

base_url = 'http://nba.sports.sina.com.cn/'


def get_all_team_url():
    url = 'http://nba.sports.sina.com.cn/players.php?'
    ret_content = requests.get(url).content
    soup = BeautifulSoup(ret_content, 'html.parser', from_encoding='utf-8')
    tags = soup.find(id='table980middle')
    a_tags_list = tags.find_all('a')
    url_dict = {}
    for item in a_tags_list:
        url_dict[item.contents[0]] = (base_url + item.attrs.get('href'))
    return url_dict


def get_team_players_data(url=None, team_name=None):
    if not url and team_name:
        team_url_dict = get_all_team_url()
        url = team_url_dict.get(team_name)

    if not url:
        return {}

    ret_content = requests.get(url).content
    soup = BeautifulSoup(ret_content, 'html.parser', from_encoding='utf-8')
    ret = soup.find(id='S_Cont_01')
    player_data_dict = {}
    for item in ret.find_all('tr')[1:-2]:
        data_dict = {}
        data_list = item.find_all('td')[1:]
        data_dict['得分'] = float(data_list[-1].contents[0])
        data_dict['篮板'] = float(data_list[-7].contents[0])
        data_dict['抢断'] = float(data_list[-5].contents[0])

        player_name = item.find('a').contents[0]
        player_data_dict[player_name] = data_dict

    return player_data_dict


def get_all_team_player_data():
    team_url_dict = get_all_team_url()
    all_team_data = {}
    for team_name, team_url in team_url_dict.items():
        team_data = get_team_players_data(team_url)
        all_team_data[team_name] = team_data

    return all_team_data


def dict2list(dic):
    keys = dic.keys()
    vals = dic.values()
    lst = [(key, val) for key, val in zip(keys, vals)]
    return lst


def get_best_data(team_data):
    team_best_data = {}
    team_data_list = dict2list(team_data)
    team_best_data['得分第一'] = sorted(team_data_list, key=lambda x: x[1]['得分'], reverse=True)[0][0]
    team_best_data['篮板第一'] = sorted(team_data_list, key=lambda x: x[1]['篮板'], reverse=True)[0][0]
    team_best_data['抢断第一'] = sorted(team_data_list, key=lambda x: x[1]['抢断'], reverse=True)[0][0]

    return team_best_data


def get_best_data_player():
    all_data_dict = get_all_team_player_data()
    team_best_player_data = {}
    for team_name, team_data in all_data_dict.items():
        team_best_data = get_best_data(team_data)
        team_best_player_data[team_name] = team_best_data

    return team_best_player_data


if __name__ == '__main__':
    #
    # data = get_all_team_player_data()
    # print(data)
    # print(player_data_dict)

    ret = get_best_data_player()
    print(ret)
    # team_data = {'布拉德利-比尔': {'得分': 22.6, '篮板': 4.4, '抢断': 1.2}, '奥托-波特': {'得分': 14.7, '篮板': 6.4, '抢断': 1.5},
    #              '凯利-乌布雷': {'得分': 11.8, '篮板': 4.5, '抢断': 1.0}, '马基夫-莫里斯': {'得分': 11.5, '篮板': 5.6, '抢断': 0.8},
    #              '约翰-沃尔': {'得分': 19.4, '篮板': 3.7, '抢断': 1.4}, '马尔辛-戈塔特': {'得分': 8.4, '篮板': 7.6, '抢断': 0.5},
    #              '迈克-斯科特': {'得分': 8.8, '篮板': 3.3, '抢断': 0.3}, '托马斯-萨托兰斯基': {'得分': 7.2, '篮板': 3.2, '抢断': 0.7},
    #              '约迪-米克斯': {'得分': 6.3, '篮板': 1.6, '抢断': 0.4}, '伊恩-马辛米': {'得分': 4.8, '篮板': 4.1, '抢断': 0.5},
    #              '蒂姆-弗雷泽': {'得分': 3.0, '篮板': 1.9, '抢断': 0.8}, '杰森-史密斯': {'得分': 3.4, '篮板': 1.6, '抢断': 0.1},
    #              '雷蒙-塞申斯': {'得分': 5.9, '篮板': 1.3, '抢断': 0.5}, '克里斯-麦考伦': {'得分': 2.4, '篮板': 1.3, '抢断': 0.0},
    #              '德文-罗宾逊': {'得分': 2.0, '篮板': 5.0, '抢断': 1.0}, '谢尔登-麦克莱伦': {'得分': 0.0, '篮板': 0.0, '抢断': 0.0},
    #              '迈克-杨': {'得分': 0.0, '篮板': 0.0, '抢断': 0.0}, '卡里克-菲利克斯': {'得分': 0.0, '篮板': 0.0, '抢断': 0.0}}
    #
    # ret = get_best_data(team_data)
    # print(ret)