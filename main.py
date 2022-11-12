import time

import vk_api
import bs4
import requests
from vk_api.utils import get_random_id
import schedule

last_post_id = 0


def write_msg(user_id, message):
    vk.messages.send(
        # peer_id = 2000000028,
        # peer_id="-217049074",
        user_id=user_id,
        random_id=get_random_id(),
        message=message
    )


token = "vk1.a.hORY0Zv8EEUislonOv9OilF0EGo80NXQWgxrmZJNBtyw-Ki9uajoig3bnKInXZ94S6eXuzTpkRcRv0Z4crbgQE9np7J7NOrbFEX6zCHeLA2eHz4dTRi0-CqUS4iuhtHLCV85OHAkdhYy9YXIKq4doGPt2t90Tk70phUkMLMxV5XUNea37cj__Ep4Ex2jJ-C3LE6hvliJ4YOPWX8uRuserQ"

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()


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

    members = vk.groups.getMembers(group_id=217049074)['items']
    print(members)
    # print(vk.wall.get(group_id="raspisanie_urtisi"))

    # index=2000000028
    # chat_info = vk.messages.getChat(chat_id=index)
    # print(chat_info)
    if post_id != last_post_id and "284" in messenge:
        last_post_id = post_id

        for i in members:
            try:
                write_msg(i, "хэй-хэй! учебный отдел опять что-то высрал! думаю, стоит чекнуть! " + post_link)
            except Exception as e:
                pass

schedule.every(5).minutes.do(get_post)
# schedule.every(100).seconds.do(get_post)
while True:
    schedule.run_pending()
    time.sleep(1)