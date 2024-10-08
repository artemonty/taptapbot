import telebot, requests, json
from token_taptap import BOTTOKEN, coins
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
bot = telebot.TeleBot(BOTTOKEN)

class CryptoConverter:
    @staticmethod
    def get_price(callback, coin):
        try:
            reqUSD = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={coins.get(coin)}&tsyms=USD")
            price_USD = json.loads(reqUSD.content)["USD"]
            reqRUB = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={coins.get(coin)}&tsyms=RUB")
            price_RUB = json.loads(reqRUB.content)["RUB"]
            text = f"Цена {coin}:\n{price_USD} USD\n{price_RUB} RUB"
            markup = InlineKeyboardMarkup()
            btnBACK = InlineKeyboardButton("Вернуться назад", callback_data="BACK")
            markup.row(btnBACK)
            bot.send_message(callback.message.chat.id, text, reply_markup=markup)
        except Exception:
            text = "Похоже, данная криптовалюта недоступна в настоящий момент."
            markup = InlineKeyboardMarkup()
            btnBACK = InlineKeyboardButton("Вернуться назад", callback_data="BACK")
            markup.row(btnBACK)
            bot.send_message(callback.message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(message):
    markup = InlineKeyboardMarkup()
    btnHMSTR = InlineKeyboardButton("Hamster Kombat", callback_data="Hamster Kombat")
    markup.row(btnHMSTR)
    btnNOT = InlineKeyboardButton("Notcoin", callback_data="Notcoin")
    btnDOGS = InlineKeyboardButton("DOGS", callback_data="DOGS")
    btnCATI = InlineKeyboardButton("Catizen", callback_data="Catizen")
    btnBlum = InlineKeyboardButton("BLUM", callback_data="BLUM")
    markup.row(btnNOT, btnDOGS, btnCATI, btnBlum)
    welcome_text = ("Привет, выбери нужную монету:")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data in coins.keys():
        coin = callback.data
        CryptoConverter.get_price(callback, coin)
    if callback.data == "BACK":
        markup = InlineKeyboardMarkup()
        btnHMSTR = InlineKeyboardButton("Hamster Kombat", callback_data="Hamster Kombat")
        markup.row(btnHMSTR)
        btnNOT = InlineKeyboardButton("Notcoin", callback_data="Notcoin")
        btnDOGS = InlineKeyboardButton("DOGS", callback_data="DOGS")
        btnCATI = InlineKeyboardButton("Catizen", callback_data="Catizen")
        btnBlum = InlineKeyboardButton("BLUM", callback_data="BLUM")
        markup.row(btnNOT, btnDOGS, btnCATI, btnBlum)
        welcome_text = ("Выбери нужную монету:")
        bot.send_message(callback.message.chat.id, welcome_text, reply_markup=markup)

bot.polling(none_stop=True)