from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
from PIL import Image, ImageDraw, ImageFont
import telebot
import os


import textwrap

load_dotenv(find_dotenv())

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN, parse_mode=None)

# {
#     chatID: {
#         userState: [],
#         messages: []
#     }
# }
userStates = {}

dimensions = {
    "1": {
        "position": (23, 300),
        "width": 10,
        "lines": 3,
        "font": 50
    },

    "2": {
        "position": (430, 50),
        "width": 10,
        "lines": 3,
        "font": 50
    },

    "3": {
        "position": (13, 720),
        "width": 10,
        "lines": 3,
        "font": 50
    },
    "4": {
        "position": (300, 800),
        "width": 20,
        "lines": 3,
        "font": 30
    },

    "5": {
        "position": (550, 600),
        "width": 10,
        "lines": 3,
        "font": 30
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chatID = message.chat.id
    basePhoto = open('images/template.jpg', 'rb')
    bot.send_photo(chatID, basePhoto)

    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("1", callback_data="option1")
    button2 = InlineKeyboardButton("2", callback_data="option2")
    button3 = InlineKeyboardButton("3", callback_data="option3")

    markup.add(button1, button2, button3)

    bot.send_message(
        chatID,
        "Choose the number to edit", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chatID = call.message.chat.id
    try: 
        userStates[chatID]
    
    except KeyError:
        userStates[chatID] = {}

    if call.data == "option1":
        bot.send_message(chatID, "Send me the text for 1")
        userStates[chatID]["userState"] = "1"

    elif call.data == "option2":
        bot.send_message(chatID, "Send me the text for 2")
        userStates[chatID]["userState"] = "2"
    
    elif call.data == "option3":
        bot.send_message(chatID, "Send me the text for 3")
        userStates[chatID]["userState"] = "3"

    elif call.data == "option4":
        bot.send_message(chatID, "Send me the text for 4")
        userStates[chatID]["userState"] = "4"
    
    elif call.data == "option5":
        bot.send_message(chatID, "Send me the text for 5")
        userStates[chatID]["userState"] = "5"

def setMessage(message, option):
    chatID = message.chat.id
    text = message.text

    try: 
        userStates[chatID]["messages"]
    
    except KeyError:
        userStates[chatID]["messages"] = []
    
    finally:
        if option == '1':
            userStates[chatID]["messages"].append(['1', text])
            userStates[chatID]["messages"].append(['4', text])
        
        elif option == '2':
            userStates[chatID]["messages"].append(['2', text])
            userStates[chatID]["messages"].append(['5', text])
        
        else:
            userStates[chatID]["messages"].append([option, text])

def drawBackground(draw, text_position, text, font, border_size=4):
    for i in range(-border_size, border_size+1):
        for j in range(-border_size, border_size+1):
            draw.text(
                (text_position[0]+i, text_position[1]+j),
                text, font=font, fill=(0,0,0)
            )

    draw.text(text_position, text, (255, 255, 255), font=font)

def generateMeme(chatID):
    img = Image.open("images/meme_one.jpg")
    draw = ImageDraw.Draw(img)
    try:
        for option, message in userStates[chatID]["messages"]:
            font = ImageFont.truetype(
                "Poppins-Black.ttf",
                dimensions[option]["font"]
            )


            text_position = dimensions[option]["position"]
            wrapper = textwrap.TextWrapper(width=dimensions[option]["width"])
            lines = wrapper.wrap(text=message)

            for line in lines:
                drawBackground(draw, text_position, line, font)
                text_position = (text_position[0], text_position[1]+60)
        
    except KeyError:
        return 2

    return img

@bot.message_handler(commands=['meme'])
def send_meme(message):
    chatID = message.chat.id
    meme = generateMeme(chatID)
    if meme == 2:
        bot.send_message(chatID, "You have not selected all the options")
        return

    bot.send_photo(chatID, meme)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chatID = message.chat.id
    if chatID not in userStates and len(userStates[chatID]) == 0:
        return

    setMessage(message, option=userStates[chatID]["userState"])
    print(userStates)

    if len(userStates[chatID]["messages"]) == 5:
        pass


bot.infinity_polling()