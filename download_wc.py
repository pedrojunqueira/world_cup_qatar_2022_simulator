import requests

url = "https://www.livesport.com/en/soccer/world/world-cup-2018/#/2/8/OneVXSrp/table"

r = requests.get(url)

with open("2018_wc.html", "w+") as fp:
    fp.write(r.text)

# with open("2018_wc.html", "r+") as fp:
#     html = fp.read()

# print(html)