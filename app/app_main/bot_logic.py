import requests
from django.conf import settings
from .models import BotUser, SearchArea, SearchResult
import telebot
from telebot import types


bot = telebot.TeleBot(settings.TG_TOKEN, parse_mode='HTML')

keys = ['Новый поиск', 'История']
request_text = 'Введите запрос:'


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):
    """
    создаем клавиатуру из списка keys
    добавляем юзера в БД, если такого еще нет
    """
    keyboard = types.ReplyKeyboardMarkup(True, row_width=2)
    keyboard.add(*keys)
    text = f'Приветствую, {message.from_user.username}!\nВыберите нужный пункт меню'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)

    BotUser.objects.get_or_create(user_id=message.chat.id)


@bot.message_handler(content_types=['text'])
def text_message(message: telebot.types.Message):
    """
    обрабатываем команды только из списка keys
    keys[0] - запуск процесса обработки пользовательского запроса
    keys[1] - вывод истории запросов
    """
    if message.text == keys[0]:
        bot.reply_to(message, text=request_text)
        bot.register_next_step_handler(message, process_user_request)
    elif message.text == keys[1]:
        requests_history = SearchResult.objects.filter(user__user_id=message.chat.id).order_by('-pk')[:5]
        if requests_history:
            text = 'История поиска:\n\n'
            for r in requests_history:
                text += f'{r.request } -> {r.result} ({r.created.strftime("%d.%m.%y")})\n\n'
        else:
            text = 'История пуста'
        bot.reply_to(message, text=text)


def process_user_request(message: types.Message):
    """
    основной алгоритм обработки пользовательского запроса
    """

    # обрабатываем запрос если он не равен значениям кнопок меню, иначе перезапускаем
    if message.text not in keys:
        user_request = message.text.replace(' ', '+')  # подготовка сообщения к передаче в URL

        request_test = f'{settings.YANDEX_BASE_URL}/?apikey={settings.YANDEX_API_KEY}' \
                       f'&geocode={user_request}&format=json'
        response_data = requests.get(request_test).json()

        addresses = response_data['response']['GeoObjectCollection']['featureMember']

        search_areas = list(SearchArea.objects.all().values_list('name', flat=True))
        area_in_list = False
        address = None
        location = None

        # перебор полученных адресов и проверка на наличие в доступных областях поиска
        for addr in addresses:
            current_area = addr['GeoObject']['metaDataProperty']['GeocoderMetaData']

            for component in current_area['Address']['Components']:
                if component['name'] in search_areas:
                    area_in_list = True
                    address = current_area['AddressDetails']['Country']['AddressLine']
                    location = addr['GeoObject']['Point']['pos'].split()
                    break
            if area_in_list:
                break

        if area_in_list:
            text = address
            # отправляем локацию для визуализации
            bot.send_location(chat_id=message.chat.id, longitude=float(location[0]), latitude=float(location[1]))
        else:
            text = 'Не найдено'

        bot.reply_to(message, text=text)

        # записываем результаты поиска в БД
        user = BotUser.objects.get_or_create(user_id=message.chat.id)[0]
        SearchResult.objects.create(user=user, request=message.text, result=text)

    else:
        bot.reply_to(message, text=request_text)
        bot.register_next_step_handler(message, process_user_request)
        return

