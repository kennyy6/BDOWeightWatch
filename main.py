import pyautogui
import telegram
import credentials
import time


def checker():
    coords = pyautogui.locateCenterOnScreen("weight.png", confidence = 0.7)
    if coords != None:
        for i in range(2):
            bot.send_message(chat_id=credentials.chat_acutal_id, text="Weight is full please restock")



    # else:
    #     # record the time
    # check a few times if the images does not exist if not check if the processes is not their
    # THen alter the user


def checkProcess():
    pass







if __name__ == "__main__":
    try:
        bot = telegram.Bot(token=credentials.api_id)
    except:
        print("ERROR COULD NOT USE BOT")

    starttime = time.time()
    timeInterval = 300# What time would you like in seconds
    while True:
        checker()
        print("test")
        time.sleep(timeInterval - ((time.time() - starttime) % 60.0))




    # while True:
    #         print(pyautogui.position())

