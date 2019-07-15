import requests

from bs4 import BeautifulSoup

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

URL = "https://www.amazon.com/Sony-Alpha-a7-III-Mirrorless/dp/B07KM942T2/ref=sr_1_8?keywords=sony+a7&qid=1562489220&s=gateway&sr=8-8"

headers = {
    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}


def send_mail(url):
    message = Mail(
        from_email='pricetracker@app.io',
        to_emails='kayode.adechinan@gmail.com',
        subject='Price fell down',
        html_content=
        '<strong>Check the amazon link : </strong>' + url)

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print("Email successfully delivered")
    except Exception as e:
        print(e.message)


def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'lxml')

    converted_price = None

    price = soup.find(id="priceblock_ourprice")

    if price:
        price = price.get_text().strip().replace('$', '')
        converted_price = float(price.replace(',', ''))

    if converted_price < 3000:
        send_mail(URL)


if __name__ == "__main__":

    check_price()
    