import requests

headers = {
    'authority': 'www.ixigua.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': "ttwid=1%7CasFh8vqf1BA_lKB4flNh6aYSOoU1BeZHe0VCVJW2gCM%7C1609405278%7C326cf22832ba04f2255c398bc6b9d2234fe1b307868558efc33a1fa1758e2a5e;",
}
# xiguavideopcwebid=6912336315766507015;
# xiguavideopcwebid.sig=3Y96Kpm0V17q4L4HP7Xo6ph_vxA;
# MONITOR_WEB_ID=da5fca13-8c48-49c7-96b1-e4f76971ef9d;
params = (
    ('wid_try', '1'),
)

response = requests.get('https://www.ixigua.com/6852564206651179534', headers=headers)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.ixigua.com/6852564206651179534?wid_try=1', headers=headers)
print(response.text)