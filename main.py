#install requests module first
import requests
from datetime import datetime
import smtplib

MY_LAT = 25.192181
MY_LONG = 75.850838
#your email id
my_email = "your email"
#your email password
my_pass = "your_password"
#your message
message = "Subject:LOOK UP\n\nISS is passing from your region"

while True:
    # making API call to iss-location now api
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")

    #to check if there is an error in api call
    iss_response.raise_for_status()

    longitude = float(iss_response.json()["iss_position"]["longitude"])
    latitude = float(iss_response.json()["iss_position"]["latitude"])
    iss_position = (longitude, latitude)

    #parameters for api
    my_pos = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        "formatted": 0
    }
    # Api call
    sun_response = requests.get("https://api.sunrise-sunset.org/json", params=my_pos)
    sun_response.raise_for_status()

    sunrise_time = sun_response.json()["results"]["sunrise"]
    sunset_time = sun_response.json()['results']["sunset"]
    sunrise_time = int(sunrise_time.split('T')[1].split(':')[0])
    sunset_time = int(sunset_time.split('T')[1].split(':')[0])
    current_time = datetime.utcnow().hour

    if current_time >= sunset_time or current_time<=sunrise_time:
        if iss_position[0]<MY_LAT+5 and iss_position[0]>MY_LAT-5 and iss_position[1]<MY_LONG+5 and iss_position[1]>MY_LONG-5:
            #send email
            #put your email id smtp code in bracate for gmail smtp code is already written
            server = smtplib.SMTP('smtp.gmail.com', 587)
            #for secure connection
            server.starttls()
            #login to your email id
            server.login(my_email,my_pass)
            #sending mail through your email id
            server.sendmail(my_email,my_email,message)
            #ending the connection
            server.quit()
            ##############
