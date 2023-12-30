from bs4 import BeautifulSoup
import requests
import smtplib
import time
import csv
import pymysql
# data urls
urls = ['https://www.amazon.in/Sony-Headphones-Customizable-Equalizer-DSEE-Upscale/dp/B09YLFHFDW/ref=dp_fod_sccl_1/260-9168887-2631746?pd_rd_w=B4kkW&content-id=amzn1.sym.fef71d27-0afa-4421-a7c1-f24b8bd4a32e&pf_rd_p=fef71d27-0afa-4421-a7c1-f24b8bd4a32e&pf_rd_r=FDJ2VSJF8WBZ1S3P0BY0&pd_rd_wg=Pgtc8&pd_rd_r=345f4db8-9403-44e9-b848-64746ad1fcdc&pd_rd_i=B09YLFHFDW&th=1',
        'https://www.amazon.in/adidas-Thick-Fitness-Carry-Strap/dp/B08K8656XQ/ref=sr_1_1_sspa?crid=3H86DVIWYA1OK&keywords=adidas+exercise+mat&qid=1703477461&sprefix=%2Caps%2C183&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1',
        'https://www.amazon.in/Fire-Boltt-Stainless-Display-Bluetooth-Assistant/dp/B0CH8BY8DG/ref=zg_bs_c_watches_sccl_2/260-9168887-2631746?pd_rd_w=X5GTf&content-id=amzn1.sym.7dd29d48-66c1-486c-967d-2ed40101f2ea&pf_rd_p=7dd29d48-66c1-486c-967d-2ed40101f2ea&pf_rd_r=V1PWCEWBMYJTYF1KY13M&pd_rd_wg=OdCGe&pd_rd_r=488b0a46-8011-4999-9a6c-228a613b6c6f&pd_rd_i=B0CH8BY8DG&th=1',
        'https://www.amazon.in/SanDisk-Ultra-Pendrive-Mobile-Warranty/dp/B0BN4468FC/ref=sr_1_2?crid=18VYUQQ88GAJ9&keywords=pendrive%2B512gb&qid=1703570286&s=computers&sprefix=pendrive%2B512%2Ccomputers%2C230&sr=1-2&th=1']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
desired_price = 3000.0
# Email credentials
sender = 'markanthony@gmail.com'
receiver = 'markanthony@gmail.com'
password = 'jshqvhinlwhiwpmh'


def extracting_data(url):
    try:
        html = requests.get(url, headers=headers)
        html.raise_for_status()
        soup = BeautifulSoup(html.content, 'lxml')
        # print(html.text)
        product_title_element = soup.find('span', id='productTitle')
        product_title = product_title_element.text.strip() if product_title_element else None
        print(f'Product Title: {product_title}')
        current_price_element = soup.find('span', class_='a-price-whole')
        current_price = float(current_price_element.text.replace(',', '')) if current_price_element else None
        print(f'Current Price: ₹{current_price}')
        availability_element = soup.find('span', class_='a-size-medium a-color-success')
        availability = availability_element.text.strip() if availability_element else None
        print(f'Availability: {availability}')
        return product_title, current_price, availability

    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None, None, None


def email_alert(product_title, current_price, url):
    message = f'Price Alert!\n {product_title} is now available for only ₹{current_price} at Amazon {url}'
    message = message.encode('utf-8')
    with smtplib.SMTP('smtp.gmail.com', 587, ) as server:
        # starttls initiates a secure transport layer security(TLS) connection over an SMTP session
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)


def storing_data_into_csv(product_title, current_price, availability, url):
    header = ['Product Title', 'Current price', 'Availability', 'URL']
    data = [product_title, current_price, availability, url]
    with open('productdata.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(header)
        writer.writerow(data)


def storing_data_into_database(product_title, current_price, availability, url):
    conn = pymysql.connect(host='localhost', user='root', password='root', database='pricemonitor', port=3306)
    cursor = conn.cursor()
    product_title = product_title[:100]
    url = url[:100]
    product_data = (product_title, current_price, availability, url)
    cursor.execute('''CREATE TABLE IF NOT EXISTS productdetails(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_title VARCHAR(400),
                    current_price INT,
                    availability VARCHAR(50),
                    url VARCHAR(400)
                    )''')
    print('Table created!')
    cursor.execute('INSERT INTO productdetails (product_title, current_price, availability, url) VALUES (%s, %s, %s, %s)', product_data)
    print('Values inserted!')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    while True:
        for url in urls:
            product_title, current_price, availability = extracting_data(url)  # Multiple assignment of variables
            if product_title is not None and current_price is not None and availability is not None:
                if current_price <= desired_price and availability == 'In stock':
                    email_alert(product_title, current_price, url)
                    storing_data_into_csv(product_title, current_price, availability, url)
                    storing_data_into_database(product_title, current_price, availability, url)
                    break
            # Pause for 10 minutes
            time.sleep(600)
