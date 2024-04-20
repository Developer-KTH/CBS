import security
from datetime import datetime, timedelta
from pytz import timezone
from requests import get, exceptions
from time import sleep
from subprocess import run

from discord import SyncWebhook, Embed
webhook = SyncWebhook.partial(security.ID(), security.Password())
embed = Embed()

url = "http://apis.data.go.kr/1741000/DisasterMsg3/getDisasterMsg1List"
params ={"serviceKey" : security.key(),
         "pageNo" : "1",
         "numOfRows" : "5",
         "type" : "json"
         }

run("clear")
print("Let's Go!")
while True:
    sleep(180)
    try:
        try:
            dataAll = get(url, params=params, timeout=30).json()["DisasterMsg"][1]["row"][::-1]
        except exceptions.Timeout:
            continue

        for data in dataAll:
            dt = timezone("Asia/Seoul").localize(datetime.strptime(str(data["create_date"]), "%Y/%m/%d %H:%M:%S"))

            if dt >= (datetime.now(timezone("Asia/Seoul")) - timedelta(minutes=3)).replace(second=0):
                embed.title = "재난안전 상황정보 #{}".format(data["md101_sn"])
                embed.url = security.url()
                embed.description = data["location_name"]
                embed.add_field(name="", value=">>> ```{}```".format(data["msg"]))
                embed.set_footer(text="{} • {}".format(data["send_platform"], data["create_date"]), icon_url=security.icon())
                webhook.send(embed=embed)
                embed.clear_fields()

    except:
        continue
