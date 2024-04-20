import security
from requests import get, exceptions
from time import sleep
from subprocess import run

from discord import SyncWebhook, Embed
webhook = SyncWebhook.partial(security.ID(), security.Password())
embed = Embed()

url = "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List"
params ={"serviceKey" : security.key(),
         "pageNo" : "1",
         "numOfRows" : "3",
         "type" : "json"
         }

run("clear")
print("Let's Go!")
nowNumber = 0
while True:
    sleep(60)
    try:
        try:
            dataAll = get(url, params=params, timeout=30).json()["DisasterMsg"][1]["row"][::-1]
        except exceptions.Timeout:
            continue

        for data in dataAll:
            if nowNumber < int(data["md101_sn"]):
                embed.title = "재난안전 상황정보 #{}".format(data["md101_sn"])
                embed.url = security.url()
                embed.description = data["location_name"]
                embed.add_field(name="", value=">>> ```{}```".format(data["msg"]))
                embed.set_footer(text="{} • {}".format(data["send_platform"], data["create_date"]), icon_url=security.icon())
                webhook.send(embed=embed)
                embed.clear_fields()

            nowNumber = int(data["md101_sn"])

    except:
        continue
