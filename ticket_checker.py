import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from bs4 import BeautifulSoup
import time

# Адрес страницы с билетами
URL = "https://www.more.com/cinema/tiff65-quasi-a-casa/"

# Заголовки, чтобы имитировать запросы как от реального пользователя
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36"
}

# Настройки для отправки почты
EMAIL_ADDRESS = "mhaidai@york.citycollege.eu"  # Укажи почту отправителя
EMAIL_PASSWORD = "350has250"           # Пароль приложения (для Gmail)
RECIPIENT_EMAIL = "nikitagaidai2018@gmail.com" # Кому отправить уведомление

def send_email():
    # Настраиваем сообщение
    subject = "Билеты доступны!"
    body = "Билеты на сайте стали доступны. Поторопитесь!"
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain"))
    
    # Настройка подключения и отправка email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print("Уведомление отправлено на почту.")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

def check_tickets():
    # Отправляем запрос к сайту
    response = requests.get(URL, headers=HEADERS)
    
    # Проверка успешного получения страницы
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Проверяем наличие элемента с помощью CSS-селектора
        tickets = soup.select_one(".booking-panel-wrap__events-container > div.vertical-align:last-of-type")
        
        if tickets:
            print("Билеты доступны! Поторопитесь!")
            send_email()  # Отправка уведомления на почту
            return True  # Чтобы можно было прервать цикл

        else:
            print("Билетов пока нет.")
    else:
        print(f"Ошибка при получении страницы, статус код: {response.status_code}")

    return False  # Продолжаем проверку

# Запускаем скрипт в цикле с паузой
while True:
    if check_tickets():
        break  # Останавливаем скрипт, если билеты появились
    time.sleep(30)  # Задержка 30 секунд между проверками
