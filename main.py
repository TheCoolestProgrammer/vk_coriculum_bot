import os
import time

import vk_api
import bs4
import requests
from flask import Flask
from vk_api.utils import get_random_id
from schedule import repeat, every

last_post_id = 0
app = Flask(__name__)

test_val = 1
@app.route("/")
@repeat(every(5).minutes)
def index():
    get_post()
    return ""
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
    # write_msg("shinomasson", "хэй-хэй! учебный отдел опять что-то высрал! думаю, стоит чекнуть! " + post_link)

def main():
    # schedule.run_pending()
    # schedule.every(1).seconds.do(get_post)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    # schedule.every(100).seconds.do(get_post)


if __name__ == '__main__':
    main()
