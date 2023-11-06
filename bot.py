import telebot
import requests
import schedule
import time

bot = telebot.TeleBot('5994935966:AAE8VMH-DwIVDC9xS3W-A6C61x9gq1Aa-i4')

start_txt = 'Привет! Это бот прогноза погоды за окном. Отправьте боту название города и он скажет, какая там температура и как она ощущается.'

# Глобальная переменная для отслеживания количества запросов
request_count = 0
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def weather(message):
    city = message.text
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=611126cbe47d90b47165019b11e8f39b'
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    weather_description = weather_data['weather'][0]['description']
    w_now = f'Сейчас в городе {city} {temperature}°C. {weather_description}'
    w_feels = f'Ощущается как {temperature_feels}°C'
    bot.send_message(message.from_user.id, w_now)
    bot.send_message(message.from_user.id, w_feels)
    wind_speed = round(weather_data['wind']['speed'])
    if wind_speed < 5:
        bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
    elif wind_speed < 10:
        bot.send_message(message.from_user.id, '🤔 На улице ветрено, лучше оденьтесь чуть теплее')
    elif wind_speed < 20:
        bot.send_message(message.from_user.id, '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
    else:
        bot.send_message(message.from_user.id, '❌ На улице шторм, на улицу лучше не выходить')

request_count += 1

def send_report():
    global request_count
    bot.send_message("2026239817", f"Number of requests today: {request_count}")
    request_count = 0

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')
# Планирование отправки отчета один раз в день в определенное время (в данном случае в 23:59)
schedule.every().day.at("23:59").do(send_report)

while True:
    schedule.run_pending()
    time.sleep(1)