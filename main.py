from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv
from PIL import Image, ImageDraw, ImageFont
import textwrap
import telebot
import os

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
        "font": 50,
        "lineWidth": 60
    },

    "2": {
        "position": (470, 50),
        "width": 10,
        "lines": 3,
        "font": 50,
        "lineWidth": 60
    },

    "3": {
        "position": (13, 720),
        "width": 10,
        "lines": 3,
        "font": 50,
        "lineWidth": 60
    },
    "4": {
        "position": (300, 800),
        "width": 20,
        "lines": 3,
        "font": 30,
        "lineWidth": 40
    },

    "5": {
        "position": (600, 600),
        "width": 10,
        "lines": 3,
        "font": 30,
        "lineWidth": 40
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global userStates

    chatID = message.chat.id
    user = message.from_user.id

    if user in userStates:
        return

    userStates = {
        user: {
            "userState": 0,
            "messages": []
        }
    }

    print(userStates)
    basePhoto = open('images/template.jpg', 'rb')
    bot.send_photo(chatID, basePhoto)

    markup = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton("1", callback_data="option1")
    button2 = InlineKeyboardButton("2", callback_data="option2")
    button3 = InlineKeyboardButton("3", callback_data="option3")

    markup.add(button1, button2, button3)

    bot.reply_to(
        message,
        "Choose the number to edit", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handleCallback(call):
    chatID = call.message.chat.id
    user = call.from_user.id

    if user not in userStates:
        print("not in")
        return

    if call.data == 'option1':
        bot.send_message(chatID, "option 1")
        userStates[user]['userState'] = 1
    
    if call.data == 'option2':
        bot.send_message(chatID, "option 2")
        userStates[user]['userState'] = 2
    
    if call.data == 'option3':
        bot.send_message(chatID, "option 3")
        userStates[user]['userState'] = 3

        
@bot.message_handler(func=lambda message: True)
def handleMessage(message):
    chatID = message.chat.id
    user = message.from_user.id

    if user not in userStates:
        print("nope")
        return

    setMessage(message, userStates[user]['userState'])

    if len(userStates[user]["messages"]) == 5:
        img = generateMeme(user)

        bot.send_photo(chatID, img)
        del userStates[user]
    

def setMessage(message, option):
    global userStates

    print(userStates)
    chatID = message.chat.id
    user = message.from_user.id

    if user not in userStates:
        print("user not in userStates")
        return

    text = message.text

    print(userStates)
    userStates[user]["messages"]

    if option == 0:
        return

    if option == 1:
        userStates[user]["messages"].append(['1', text])
        userStates[user]["messages"].append(['4', text])

        userStates[user]["userState"] = 0
        # bot.send_message(chatID, "Noted")
        bot.reply_to(message, "Noted")
        
    elif option == 2:
        userStates[user]["messages"].append(['2', text])
        userStates[user]["messages"].append(['5', text])

        userStates[user]["userState"] = 0
        bot.reply_to(message, "Noted")
        # bot.send_message(chatID, "Noted")

        
    else:
        userStates[user]["messages"].append([str(option), text])
        userStates[user]["userState"] = 0
        # bot.send_message(chatID, "Noted")
        bot.reply_to(message, "Noted")


def drawBackground(draw, text_position, text, font, border_size=4):
    for i in range(-border_size, border_size+1):
        for j in range(-border_size, border_size+1):
            draw.text(
                (text_position[0]+i, text_position[1]+j),
                text, font=font, fill=(0,0,0)
            )

    draw.text(text_position, text, (255, 255, 255), font=font)

def generateMeme(user):
    img = Image.open("images/meme_one.jpg")
    draw = ImageDraw.Draw(img)
 
    for option, message in userStates[user]['messages']:
        print(dimensions[option]['font'])
        font = ImageFont.truetype(
            "Poppins-Black.ttf",
            dimensions[option]["font"]
        )

        text_position = dimensions[option]["position"]
        wrapper = textwrap.TextWrapper(width=dimensions[option]["width"])
        lines = wrapper.wrap(text=message)

        # print(lines)
        for line in lines:
            drawBackground(draw, text_position, line, font)
            text_position = (
                text_position[0],
                text_position[1]
                + dimensions[option]["lineWidth"]
            )

    return img

bot.infinity_polling()