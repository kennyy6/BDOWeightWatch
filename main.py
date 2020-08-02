import pyautogui
import telegram
from telegram.ext import Updater, CommandHandler,CallbackQueryHandler,MessageHandler, Filters
import time
import os
try:
    import credentials
except ModuleNotFoundError:
    print("Please provide your own credential ID for telegram api key")


class bdo_model:

    def __init__(self):
        try:
            self.bot = telegram.Bot(token=credentials.api_id)
        except:
            print("ERROR COULD NOT USE BOT")

        self.response = Updater(credentials.api_id, use_context=True)
        # Provide Handler for Shutdown
        self.response.dispatcher.add_handler(CommandHandler("shutdown", self.pc_shutDown_warning))
        # Handler for start
        self.response.dispatcher.add_handler(CommandHandler("start", self.start))

        # Handlers in Reponse for confirmation of YES to shutdown or No to shutdown
        self.response.dispatcher.add_handler(CallbackQueryHandler(self.button))

        self.response.start_polling()
        # Just a Notification to show that the bot is actually working.
        self.bot.send_message(chat_id=credentials.chat_acutal_id, text="Bot is running start by typing '/start' " )

        #Initialize it as False by default will request user to amount of time required to call self.check_weight or self.check_cooking

        self.verify_time = False
        #self.response.idle()

    def start(self, update, context):
        """
        Finds out the user what they want to do with this python script either for tracking max weight
        or either when they have finished what they are doing

        Note to self also provide at what frequency would they like to do it.
        """

        # bot.send_message(chat_id=credentials.chat_acutal_id,text = "Are you sure you want to shut down computer?")
        keyboard = [[telegram.InlineKeyboardButton("max weight", callback_data='max_weight'),
                     telegram.InlineKeyboardButton("cooking utensil durability usage", callback_data='max_cooking'),
                     telegram.InlineKeyboardButton("Both", callback_data='both_max'),
                     telegram.InlineKeyboardButton("Neither", callback_data='both_none')]]
        reply_keyboard = telegram.InlineKeyboardMarkup(keyboard)

        update.message.reply_text('What would you like to keep track of', reply_markup=reply_keyboard)
        return

    def pc_shutDown_warning(self,update,context):
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



    def pc_shutdown(self):
        os.system('shutdown -s')

    def button(self,update, context):
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed

        print(query.data)
        if query.data == "True_to_Shutdown":
            self.pc_shutdown()
        elif query.data == "False_to_Shutdown":
            query.edit_message_text(text="Okay I will not shutdown pc :)")

        elif query.data == 'max_weight':
            self.max_weight = True
            self.max_cooking = False
            self.verify_time = True
        elif query.data == 'max_cooking':
            self.max_cooking = True
            self.max_weight = False
            self.verify_time = True

        elif query.data == 'both_max':
            self.max_cooking = True
            self.max_weight = True
            self.verify_time = True

        elif query.data =='both_none':
            self.max_cooking = False
            self.max_weight = False
            self.verify_time = False

        if self.verify_time:
            print(self.verify_time)
            query.edit_message_text(text="How much time would you like (in seconds)?")

            # Note to self you might have to stop the bot, then start it again
            # Add a conversation Handler so i can get their response
            self.response.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,self.time_give))

    def time_give(self,update,context):
        messsage =update.message.text
        print("Message Received: ",update.message.text," seconds will be the timer")
        try:
            timer =int(messsage)
        except:
            update.message.reply_text("Cannot convert to Integer")
            return

        self.loop(timer)

    def loop(self,timer):
        """
        Repeatedly Check based on a timer provided by the user
        """

        while self.verify_time:
            print(self.verify_time)
            if self.max_weight:
                print("called check_weight Function")
                self.check_weight()
            if self.max_cooking:
                print("called max_cooking function")
                self.check_cooking()
            time.sleep(timer)



    def open_bdo(self):
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

    def check_weight(self):
        """
        Scans to screen to see if the weight limit exist
        :return:
        """

        if self.checkProcess(): # checks to see whether if bdo.exe processor exist

            coords = pyautogui.locateCenterOnScreen("bdo_weight.png", confidence = 0.7)
            if coords == None:
                # if cant find coordinates then maybe its minimised so we open it up
                self.open_bdo()
                time.sleep(5)
                coords = pyautogui.locateCenterOnScreen("bdo_weight.png", confidence=0.5)


            if coords != None:
                #pyautogui.moveTo(coords.x,coords.y)
                for i in range(2):
                    print("Sent Message: BDO Weight is full", )
                    self.bot.send_message(chat_id=credentials.chat_acutal_id, text="Weight is full please restock")

        else:
            print("Sent Message: BDO is not running",)
            self.bot.send_message(chat_id=credentials.chat_acutal_id,text="Black Desert.exe isn't running")

        return

    def check_cooking(self):
        """
        Check cooking utensil usage, when durability has finished bdo_cooking_icon.png should come out of
        utenisil. Thus, you need to set it up where your about to begin cooking you see something like the image.
        """
        if self.checkProcess():  # checks to see whether if bdo.exe processor exist
            coords = pyautogui.locateCenterOnScreen("bdo_cooking_icon.png", confidence=0.4)
            if coords == None:
                self.open_bdo()
                time.sleep(5)
                coords = pyautogui.locateCenterOnScreen("bdo_cooking_icon.png", confidence=0.4)

            if coords != None:
                self.bot.send_message(chat_id=credentials.chat_acutal_id, text="Cooking is now finished!!!!")




    def checkProcess(self):
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








if __name__ == "__main__":
    run = bdo_model()





