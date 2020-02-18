import pyautogui
import telegram
import credentials
import time
import os



def checker():
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


def checkProcess(name):
    #print(os.popen('BlackDesert64').read())
    r = os.popen('tasklist /v').read().strip().split('\n')

    for i in range(len(r)):
        if name in r[i]:
            print(r[i])
            print('%s in r[i]' % (name))
            return True

    shutdown = False
    if shutdown:
        pc_shutDown()

def pc_shutDown():
    os.system('shutdown -s')












if __name__ == "__main__":
    # try:
    #     bot = telegram.Bot(token=credentials.api_id)
    # except:
    #     print("ERROR COULD NOT USE BOT")
    #
    # starttime = time.time()
    # timeInterval = 60# What time would you like in seconds
    # while True:
    #     checker()
    #     print("test")
    #     time.sleep(timeInterval - ((time.time() - starttime) % 60.0))
    #
    #

    checkProcess("BlackDesert64")