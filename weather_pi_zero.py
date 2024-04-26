#pip3 install numpy 
#pip3 install requests-cache retry-requests numpy pandas
#pip3 install pillow
#fonts location: /usr/share/fonts/truetype

#
import requests

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from datetime import date
import datetime

url = "https://api.open-meteo.com/v1/forecast"

params = {
	"latitude": 59.4136,
	"longitude": 17.8687,
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m", "wind_direction_10m"],
	"hourly": ["temperature_2m", "apparent_temperature", "precipitation_probability", "weather_code", "wind_speed_10m","is_day"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "precipitation_probability_max"],
	"timezone": "Europe/Berlin",
	"past_hours": 1,
	"forecast_days": 8,
	#"forecast_minutely_15": 48
}

weather_code_descriptions ={
        "0":"Clear Sky"        
        ,"1":"Mainly Clear"
        ,"2":"Partly Cloudy"
        ,"3":"Overcast"
        ,"45":"Fog"
        ,"48":"Fog"
        ,"51":"Light Rain"
        ,"53":"Moderate Rain"
        ,"55":"Dense Rain"
        ,"56":"Freezing Rain"
        ,"57":"Freezing Rain"
        ,"61":"Slight Rain"
        ,"63":"Moderate Rain"
        ,"65":"Heavy Rain"
        ,"66":"Freezing Rain"
        ,"67":"Heavy Rain "
        ,"71":"Slight Snow"
        ,"73":"Moderate Snow"
        ,"75":"Heavy Snow"
        ,"77":"Snow Grains"
        ,"80":"Slight Rain"
        ,"81":"Moderate Rain"
        ,"82":"Heavy Rain"
        ,"85":"Snow Rain"
        ,"86":"Snow Rain"
        ,"95":"Thunderstorm"
        ,"96":"Thunderstorm"
        ,"99":"Thunderstorm"
}

api_response = requests.get(url = url , params=params).json()

curernt_weather_date = api_response['current']['time'][0:10]
current_temperature = api_response['current']['temperature_2m']
real_feel_current = api_response['current']['apparent_temperature'] 
current_humidity = str(api_response['current']['relative_humidity_2m']) + '%'
current_weather_code = str(api_response['current']['weather_code'])
current_cloud_cover = str(api_response['current']['cloud_cover']) + '%'
current_wind_speed = api_response['current']['wind_speed_10m']
current_wind_direction= api_response['current']['wind_direction_10m']
current_is_day = api_response['current']['is_day'] 
current_sunrise = api_response['daily']['sunrise'][0][11:]
current_sunset =api_response['daily']['sunset'][0][11:]

if current_weather_code == '0' and current_is_day == 0:
    current_weather_code = '00'

if (current_weather_code == '1' or current_weather_code == '')  and current_is_day == 0:
    current_weather_code = '22'

weather_data_png = Image.new(mode="RGB", size=(800, 480), color=("White" ))
myFont = ImageFont.truetype('LiberationSans-Bold.ttf', 15)
weather_image = ImageDraw.Draw(weather_data_png)


weather_image.text((15, 10), "Järfälla , Stockholm Sweden",font=myFont, fill=(0, 106, 188))
weather_image.text((15, 31), date.today().strftime('%A %B, %d'),font=myFont, fill=(0, 106, 188))


# main weather display, current conditions
main_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+current_weather_code+'.png')
weather_data_png.paste(main_weatehr_icon,(30,50),mask=main_weatehr_icon)

weather_image.text((65, 180)
                   ,str(current_temperature)+ ' °C'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 30)
                   , fill=(0, 106, 188))
weather_image.text((50, 220)
                   ,'Feels like '+str(real_feel_current)+ ' °C'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))
weather_image.text((50, 240)
                   ,weather_code_descriptions[str(api_response['current']['weather_code'])]
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                  , fill=(0, 106, 188))

main_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+'sunrise'+'.png')
main_weatehr_icon = main_weatehr_icon.resize((70,70))
weather_data_png.paste(main_weatehr_icon,(15,270),mask=main_weatehr_icon)

weather_image.text((100, 300)
                   ,current_sunrise
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))


main_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+'sunset'+'.png')
main_weatehr_icon = main_weatehr_icon.resize((70,70))
weather_data_png.paste(main_weatehr_icon,(15,340),mask=main_weatehr_icon)

weather_image.text((100, 370)
                   ,current_sunset
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))                  

main_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+'wind_1'+'.png')
main_weatehr_icon = main_weatehr_icon.resize((55,55))
weather_data_png.paste(main_weatehr_icon,(18,415),mask=main_weatehr_icon)

weather_image.text((100, 435)
                   ,str(current_wind_speed)+' km/h'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))


#daily forecasts
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ,"Sunday"]

x = 240
for i in range(1,7):
    
    weather_image.text((x+35, 10)
                   ,days[datetime.datetime.strptime(str(api_response['daily']['time'][i][0:10]),'%Y-%m-%d').date().weekday()][0:3]
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(174, 55, 86))
    
    weather_image.text((x+25, 45)
                   ,str(api_response['daily']['temperature_2m_max'][i]) + '° | ' + str(api_response['daily']['temperature_2m_min'][i]) +'°'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))    
    
    daily_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+str(api_response['daily']['weather_code'][i])+'.png')
    daily_weatehr_icon = daily_weatehr_icon.resize((90,90))
    weather_data_png.paste(daily_weatehr_icon,(x,70),mask=daily_weatehr_icon)    

    weather_image.text((x+25, 180)
                   ,str(api_response['daily']['apparent_temperature_min'][i]) + '° | ' + str(api_response['daily']['temperature_2m_min'][i])+'°'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))  
    
    weather_image.text((x+35, 210)
                   ,str(api_response['daily']['precipitation_probability_max'][i]) + '%'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))   
    
    weather_image.text((x+20, 240)
                   ,weather_code_descriptions[str(api_response['daily']['weather_code'][i])]
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 12)
                   , fill=(255, 165, 0))     
    x=x+90


j=0
for i in api_response['hourly']['time']:
    if i >= api_response['current']['time']:
        break            
    j=j+1
   
#if str(api_response['hourly']['weather_code'][j]) == '0' and api_response['hourly']['is_day'][j] == 0:
#    weather_code = '00'
#else:
#    weather_code=str(api_response['hourly']['weather_code'][j])

#if (str(api_response['hourly']['weather_code'][j]) == '1' or str(api_response['hourly']['weather_code'][j]) == '2')  and api_response['hourly']['is_day'][j] == 0:
#    weather_code = '22'      
#else:
#    weather_code=str(api_response['hourly']['weather_code'][j])

#main_weatehr_icon = Image.open('icons/'+weather_code+'.png')
#weather_data_png.paste(main_weatehr_icon,(30,50),mask=main_weatehr_icon)

#weather_image.text((50, 240)
#                   ,weather_code_descriptions[str(api_response['hourly']['weather_code'][j])]
#                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
#                   , fill=(0, 106, 188))

x=240
for i in range(0,6):
    weather_image.text((x+35, 280)
                   ,api_response['hourly']['time'][j+i].split('T')[1]
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(174, 55, 86))   
    
    weather_image.text((x+45, 300)
                   ,str(api_response['hourly']['temperature_2m'][j+i]) + '°'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))   

    if str(api_response['hourly']['weather_code'][j+i]) == '0' and api_response['hourly']['is_day'][j+i] == 0:
        weather_code = '00'
    else:
        weather_code=str(api_response['hourly']['weather_code'][j+i])

    if (str(api_response['hourly']['weather_code'][j+i]) == '1' or str(api_response['hourly']['weather_code'][j+i]) == '2')  and api_response['hourly']['is_day'][j+i] == 0:
        weather_code = '22'      
    else:
        weather_code=str(api_response['hourly']['weather_code'][j+i])

    daily_weatehr_icon = Image.open('/home/umair/Documents/info_dashboard/icons/'+weather_code+'.png')
    daily_weatehr_icon = daily_weatehr_icon.resize((60,60))
    weather_data_png.paste(daily_weatehr_icon,(x+30,320),mask=daily_weatehr_icon)  

    weather_image.text((x+45, 390)
                   ,str(api_response['hourly']['apparent_temperature'][j+i]) + '°'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188)) 
    weather_image.text((x+45, 410)
                   ,str(api_response['hourly']['precipitation_probability'][j+i]) + '%'
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 15)
                   , fill=(0, 106, 188))
    weather_image.text((x+30, 435)
                   ,weather_code_descriptions[str(api_response['hourly']['weather_code'][j+i])]
                   ,font=ImageFont.truetype('LiberationSans-Bold.ttf', 12)
                   , fill=(0, 106, 188))

    x=x+90


weather_data_png.save("weather.png")    


