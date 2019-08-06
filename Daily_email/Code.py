#Simple automated email, with some comics picture, current weather + weather forecast

import os, bs4, requests
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import json


EMAIL = input("Enter your email address")
PASSWORD = input("Enter the password here")
strFrom = input("Enter the sender email's address")
strTo = input("Enter the recipient email's address")

os.makedirs("D:\\Dummy", exist_ok=True)         #create the folder Dummy in :\\D, if necessary
os.chdir("D:\\Dummy")

#COMICS PART
savage_data = requests.get("https://www.savagechickens.com/")
soup = bs4.BeautifulSoup(savage_data.text, features="lxml")
images = soup.find("div", class_="entry_content").p.img
url_image = images.get('src')
last_part_url_image = url_image.split('/')[5]
picture = requests.get(url_image)

#checks the latest image of the comics blog and updates status (1= update, 0= no update)
status_chicken = 0
try:
    f = open("D:\\Dummy\\{}".format(last_part_url_image), "rb")
except Exception:
    with open("D:\\Dummy\\{}".format(last_part_url_image), "wb") as last_image:
        for chunck in picture.iter_content(10000):
            last_image.write(chunck)
    status_chicken = 1
    message_chicken = "Here is a new chicken comic picture"
else:
    status_chicken = 0
    message_chicken = "There is no chicken comic picture today"
    f.close()

#Getting the image from xkcd.com
xkcd = requests.get("https://xkcd.com/")
soup_xkcd = bs4.BeautifulSoup(xkcd.text, features="lxml")
images_xkcd = soup_xkcd.find("div", id="comic").img
url_image_xkcd = images_xkcd.get("src")
last_part_url_xkcd = url_image_xkcd.split("/")[4]
picture_xkcd = requests.get("https:{}".format(url_image_xkcd))

#checks the latest image of the comics blog and updates status (1= update, 0= no update)
status_xkcd = 0
try:
    f = open("D:\\Dummy\\{}".format(last_part_url_xkcd), "rb")
except Exception:
    with open("D:\\Dummy\\{}".format(last_part_url_xkcd), "wb") as last_image_xkcd:
        for chunck in picture_xkcd.iter_content(10000):
            last_image_xkcd.write(chunck)
    status_xkcd = 1
    message_xkcd = "Here is a new xkcd comic picture"
else:
    status_xkcd = 0
    message_xkcd = "There is no xkcd comic picture today"
    f.close()


#WEATHER FORECAST for BERLIN

API_key = input("Enter your API_key from https://home.openweathermap.org")           #register here to get your API_key: https://home.openweathermap.org/
api_current_info = requests.get("http://api.openweathermap.org/data/2.5/weather?id=2950157&APPID={}".format(API_key)).text
api_forecast_info = requests.get("http://api.openweathermap.org/data/2.5/forecast?id=2950157&APPID={}".format(API_key)).text

#Current weather
dico_cu_weather = json.loads(api_current_info)
temperature_cu = round(dico_cu_weather["main"]["temp"]-273.15,2)
humidity_cu = dico_cu_weather["main"]["humidity"]
weather_description_cu = dico_cu_weather["weather"][0]["description"]
cu_weather_message = "Current weather is: {}°C, {}% of humidity and {}.".format(temperature_cu, humidity_cu, weather_description_cu)


#Weather forecast
pyth_fc = json.loads(api_forecast_info)
dico_weather = pyth_fc["list"]

#forecast: 3-4 hours and 6-7 hours


Berlin_weather_fc = []
for i in range(x,y):
    time_forecast = dico_weather[i]["dt_txt"]
    temperature = round(dico_weather[i]["main"]["temp"]-273.15, 2)
    humidity = dico_weather[i]["main"]["humidity"]
    weather_description = dico_weather[i]["weather"][0]["description"]
    Berlin_weather_fc.append("Weather on {} is: {}°C, {}% of humidity and {}.".format(time_forecast, temperature, humidity, weather_description))


dt = datetime.datetime.now()
dt_email = dt.strftime('%A %d %B of %Y')



msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = "Good morning! News of {}".format((dt_email))
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = "This is the morning email"

msgText = MIMEText('{}<br><img src="cid:0"><br>{}<br><img src="cid:1"><br>{}<br>{}<br>{}Enjoy the day!'.format(message_chicken, message_xkcd, cu_weather_message, Berlin_weather_fc[0], Berlin_weather_fc[1]), 'html')  #embed the image + text
msgRoot.attach(msgText)

if status_chicken == 1:
    with open(last_part_url_image, 'rb') as im:
        msgImage = MIMEImage(im.read())
        msgImage.add_header('Content-ID', '<0>')
        msgRoot.attach(msgImage)

if status_xkcd == 1:
    with open(last_part_url_xkcd, 'rb') as im_xkcd:
        msgImage_xkcd = MIMEImage(im_xkcd.read())
        msgImage_xkcd.add_header('Content-ID', '<1>')
        msgRoot.attach(msgImage_xkcd)


#smtp object settup
smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
smtp_obj.ehlo()
smtp_obj.starttls()
smtp_obj.login(EMAIL, PASSWORD)
smtp_obj.sendmail(strFrom, strTo, msgRoot.as_string())
smtp_obj.quit()




""": Next steps:

#3: ADD http://www.lunarbaboon.com/: OPTIONAL

#4: take the current weather: API

https://openweathermap.org/api
#5: take the forecast weather for tomorrow: API
https://openweathermap.org/api

#6: add a random quote, from dictionnary?

"""





