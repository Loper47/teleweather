import pyowm
import telebot
# от блокировок
# from telebot import apihelper
# apihelper.proxy = {'https':'socks5://127.0.0.1:9050'}

owm=pyowm.OWM('6d00d1d4e704068d70191bad2673e0cc', language = 'ru')

bot = telebot.TeleBot('1005511822:AAEZjkuovcgxYwhKu9lVvMSxYkpu4SrL1CQ')


@bot.message_handler(content_types=['text'])
def send_echo(message):
  if message.text == '/start':
    answer1 = 'Привет! Чтобы узнать погоду, просто пришли мне название любого города!'
    bot.send_message(message.chat.id, answer1)
  else:

    try:
      observation = owm.weather_at_place(message.text)
      w = observation.get_weather()
      temp=w.get_temperature('celsius')['temp']

      answer = f"В городе {message.text} сейчас {w.get_detailed_status()} \n"
      answer += f"Температура в районе {round(temp)} градусов\n\n"

      if temp<10:
        answer += 'Очень холодно, оденься потеплее))'
      elif temp<18:
        answer += 'Прохладно, лучше оденься:)'
      else:
        answer += 'Не холодно, хоть в трусах иди:)'

      bot.send_message(message.chat.id, answer)
    except pyowm.exceptions.api_response_error.NotFoundError:
      exanswer = 'Город не найден :(\n'
      exanswer += 'Повторите попытку'
      bot.send_message(message.chat.id, exanswer)
      

bot.polling(none_stop = True)