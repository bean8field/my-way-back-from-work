
import requests
from bs4 import BeautifulSoup as bs
import re

url = "https://www.smpa.go.kr/user/nd54882.do"

BOARD_NO_FORMAT = re.compile(r"\d{8}")

bot_token = "6158689346:AAEcn7OyGFfk6DjhyN25TjzGs5GEuTxVNE8"

def main():
    list_page_response = requests.get(url)

    if list_page_response.status_code != 200:
        exit(1)

    list_page_html = list_page_response.text
    soup = bs(list_page_html, 'html.parser')
    attach_info = soup.select_one('#subContents > div > div.inContent > table > tbody > tr:nth-child(1) > td.subject > a')

    title = attach_info.text.strip()
    board_no = BOARD_NO_FORMAT.findall(attach_info.attrs.get('href'))[0]
    download_url = f"https://www.smpa.go.kr/user/nd54882.do?View&uQ=&pageST=SUBJECT&pageSV=&imsi=imsi&page=1&pageSC=SORT_ORDER&pageSO=DESC&dmlType=&boardNo={board_no}&returnUrl=https://www.smpa.go.kr:443/user/nd54882.do#attachdown"

    today_response = requests.get(download_url)
    today_page_html = today_response.text
    image_path = bs(today_page_html, 'html.parser').select_one('#subContents > div > div.inContent > div > div > img').attrs.get('src')

    image_download_url = "https://www.smpa.go.kr" + image_path

    image_response = requests.get(image_download_url)
    if image_response.status_code != 200:
        exit(1)

    chat_id = "6442525387"
    webhook_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto?chat_id={chat_id}"

    response = requests.post(webhook_url, files={'photo': image_response.content})
    print(response.status_code)


if __name__ == "__main__":
    main()
