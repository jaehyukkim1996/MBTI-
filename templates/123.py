import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.personality-database.com/profile?pid=1&sort=top',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

mbtis= soup.select_one('#root > div > section > main > div.rc-row > div.rc-col.rc-col-9 > div.profile > div.profile-container > a:nth-child(5) > div > div.info > h2')
print(mbtis)



#
#     print (mbtis)
#
#     # for mbti in mbtis:
#     #     a_tag=mbti.select_one('div > div.info > h2')
#     #
