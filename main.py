import time

import vk_api
import bs4
import requests
from vk_api.utils import get_random_id
import schedule

last_post_id = 0

def write_msg(user_id, message):
    try:
        x = int(user_id)
        vk.messages.send(
            # peer_id = 2000000028,
            # peer_id="-217049074",
            user_id=x,
            random_id=get_random_id(),
            message=message
        )
    except Exception as e:
        vk.messages.send(
            # peer_id = 2000000028,
            # peer_id="-217049074",
            domain=user_id,
            random_id=get_random_id(),
            message=message
        )


token = "vk1.a.hORY0Zv8EEUislonOv9OilF0EGo80NXQWgxrmZJNBtyw-Ki9uajoig3bnKInXZ94S6eXuzTpkRcRv0Z4crbgQE9np7J7NOrbFEX6zCHeLA2eHz4dTRi0-CqUS4iuhtHLCV85OHAkdhYy9YXIKq4doGPt2t90Tk70phUkMLMxV5XUNea37cj__Ep4Ex2jJ-C3LE6hvliJ4YOPWX8uRuserQ"

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

@schedule.repeat(schedule.every(5).minutes)
def get_post():
    global last_post_id
    request = requests.get("https://vk.com/raspisanie_urtisi")
    bs = bs4.BeautifulSoup(request.text, "html.parser")

    wall_items = bs.findAll('div', class_="wall_item")
    x = wall_items[1].find("a")
    post_id = int(x.attrs["name"].split("-")[1])

    x = wall_items[1].find('div', class_="wi_info").find("a")
    post_link = "https://vk.com/raspisanie_urtisi?w=" + x.attrs["href"][1:]

    messenge = wall_items[1].find("div", class_="pi_text")
    messenge = str(messenge).split(">")[1].split("<")[0].lower()
    members = vk.groups.getMembers(group_id=217049074)['items']
    # print(vk.wall.get(group_id="raspisanie_urtisi"))

    # index=2000000028
    # chat_info = vk.messages.getChat(chat_id=index)
    # print(chat_info)

    if post_id != last_post_id:
        last_post_id = post_id

        new_messenge=""
        if "284" in messenge:
            new_messenge= "хэй-хэй! учебный отдел опять что-то высрал! думаю, стоит чекнуть! "
        if "бурумбаев" in messenge and "адил" in messenge:
            new_messenge = "учебный отдел написал что-от об Адиле(математика\физика) "
        elif "чуркин" in messenge:
            new_messenge= "учебный отдел написал что-то о Чуркине(русский) "
        elif "белобородов" in messenge:
            new_messenge= "учебный отдел написал что-то о Белобородовой(инфа) "
        elif "савин" in messenge:
            new_messenge= "учебный отдел написал что-то о Савиной(общество) "
        elif "лаврентьев" in messenge:
            new_messenge= "учебный отдел написал что-то о Лаврентьевой(англ 2 группа) "
        elif "шабуров" in messenge:
            new_messenge= "учебный отдел написал что-то о Шабуровой(история) "
        
        if new_messenge:
            new_messenge += post_link
            for i in members:
                try:
                    write_msg(i, new_messenge)
                except Exception as e:
                    pass

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)