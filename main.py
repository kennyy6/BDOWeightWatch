import pyautogui
import telegram
from telegram.ext import Updater, CommandHandler,CallbackQueryHandler
import time
import os
try:
    import credentials
except ModuleNotFoundError:
    print("Please provide your own credential ID for telegram api key")


def open_bdo():
    """
    Opens up Bdo in the event if it is currently not opened.
    :return:
    """

    coords = pyautogui.locateCenterOnScreen("bdo_icon.png", confidence=0.7)
    if coords != None:
        pyautogui.click(coords.x, coords.y)
        return True
    # Check if its actually minimised so with another icon

    coords = pyautogui.locateCenterOnScreen("show_hidden_icon.png", confidence=0.7)
    if coords != None:
        pyautogui.click(coords.x,coords.y)
        coords = pyautogui.locateCenterOnScreen("bdo_icon_2.png", confidence=0.7)
        if coords != None:
            pyautogui.click(coords.x, coords.y)
    return False

def checker():
    """
    Scans to screen to see if the weight limit exist
    :return:
    """

    check_opened = open_bdo()


    coords = pyautogui.locateCenterOnScreen("bdo_weight.png", confidence = 0.7)
    if coords == None:
        time.sleep(5)
        coords = pyautogui.locateCenterOnScreen("bdo_weight.png", confidence=0.5)


    if coords != None and check_opened:
        print("sent message")
        pyautogui.moveTo(coords.x,coords.y)
        for i in range(2):
            bot.send_message(chat_id=credentials.chat_acutal_id, text="Weight is full please restock")


    # else:
    #     # record the time
    # check a few times if the images does not exist if not check if the processes is not their
    # THen alter the user


def checkProcess():
    """
    Checks to see if blackdesert64.exe still exists within the task manager
    :param name:
    :return:
    """
    #print(os.popen('BlackDesert64').read())
    r = os.popen('tasklist /v').read().strip().split('\n')
    name = "BlackDesert64"
    for i in range(len(r)):
        if name in r[i]:
            # print(r[i])
            # print('%s in r[i]' % (name))
            return True


    return False

def pc_shutDown_warning(update,context):
    """
    Verifys with the user to see if they whether want to shut down the pc.

    :return:
    """
    #bot.send_message(chat_id=credentials.chat_acutal_id,text = "Are you sure you want to shut down computer?")
    keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='True_to_Shutdown'),
                 telegram.InlineKeyboardButton("No", callback_data='False_to_Shutdown')]]
    reply_keyboard = telegram.InlineKeyboardMarkup(keyboard)
    print("test")
    update.message.reply_text('Are you sure you want to shut down computer?', reply_markup=reply_keyboard)
    return

def pc_shutdown():
    os.system('shutdown -s')

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    print(query.data)
    if query.data == "True_to_Shutdown":
        pc_shutdown()
    elif query.data == "False_to_Shutdown":
        query.edit_message_text(text="Okay I will not shutdown pc :)")


def test(update,context):
    update.message.reply_text(update.message.text)
    #bot.send_message(chat_id=credentials.chat_acutal_id, text="HI")





if __name__ == "__main__":


    try:
        bot = telegram.Bot(token=credentials.api_id)
    except:
        print("ERROR COULD NOT USE BOT")



    response = Updater(credentials.api_id, use_context = True)
    # Provide Handler for Shutdown
    response.dispatcher.add_handler(CommandHandler("shutdown",pc_shutDown_warning))
    # Handlers in Reponse for confirmation of YES to shutdown or No to shutdown
    response.dispatcher.add_handler(CallbackQueryHandler(button))

    response.start_polling()
    # Just a Notification to show that the bot is actually working.
    bot.send_message(chat_id=credentials.chat_acutal_id, text="Bot is running")
    x = int(input("Value ?"))
    while True:
        checker()
        time.sleep(x)
    #response.idle()


