import pyautogui
import telegram
from telegram.ext import Updater, CommandHandler
import time
import os
try:
    import credentials
except ModuleNotFoundError:
    print("Please provide your own credential ID for telegram api key")


def checker():
    """
    Scans to screen to see if the weight limit exist
    :return:
    """
    coords = pyautogui.locateCenterOnScreen("weight.png", confidence = 0.7)
    print(coords)
    if coords != None:
        print("sent message")
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

    shutdown = False
    if shutdown:
        pc_shutDown()
    return False

def pc_shutDown():
    os.system('shutdown -s')

def test(update,context):
    update.message.reply_text(update.message.text)
    #bot.send_message(chat_id=credentials.chat_acutal_id, text="HI")


if __name__ == "__main__":
    try:
        bot = telegram.Bot(token=credentials.api_id)
    except:
        print("ERROR COULD NOT USE BOT")

    response = Updater(credentials.api_id, use_context = True)
    response.dispatcher.add_handler(CommandHandler("test",test))
    response.start_polling()
    response.idle()


    # starttime = time.time()
    # timeInterval = 180# What time would you like in seconds
    # while True:
    #     checker() # Checks weight Limit
    #     time.sleep(timeInterval - ((time.time() - starttime) % 60.0))
    #     processcheck = checkProcess()
    #     if processcheck:
    #         print("Black desert is running")
    #     else:
    #         print("Black desert is not running")
    #         bot.send_message(chat_id=credentials.chat_acutal_id, text="Black Desert Process in not running")
    #
    #
