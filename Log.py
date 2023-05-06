import datetime
import os
from cryptography.fernet import Fernet
import secret

class Log:
    text_gray_on_black = "\033[1;30;40m"
    text_red_on_black = "\033[1;31;40m"
    text_green_on_black = "\033[1;32;40m"
    text_orange_on_black = "\033[1;33;40m"
    text_blue_on_black = "\033[1;34;40m"
    text_purple_on_black = "\033[1;35;40m"
    text_white_on_black = "\033[1;37;40m"
    enable_file_output = True       #set to True to record log output to a file
    log_dir = "log"                 #the name of the directory to store log files to
    encrypt_file = True             #if True then all data saved to the log is encrypted
    log_expiration_days = 30        #after this many days, old log files will be deleted

    @staticmethod
    def get_timestamp():
        return str(datetime.datetime.now()).replace(":", "-")
    
    @staticmethod
    def get_date():
        return str(datetime.datetime.today().strftime('%Y-%m-%d'))
    
    @staticmethod
    def write_to_file(message, type=None, filename=None):
        message = Log.remove_colors(message)

        if type == None:
            message = now + " " + message
        elif type == ",":
            message = now + "," + message       #helps with generating csv files
        else:
            message = now + " " + type + " " + message

        if Log.encrypt_file:
            cipher_suite = Fernet(secret.ENCRYPTION_KEY)
            message = str(cipher_suite.encrypt(bytes(message, "utf-8")))
        
        if filename == None:
            filename = os.path.join(os.getcwd(), Log.log_dir, Log.get_date() + ".log")

        f = open(filename, "a")
        f.write(message + "\n")
        f.close()

        Log.check_for_old_logs()

    @staticmethod
    def check_for_old_logs():
        #calculate the expiration date (today minus log_expiration_days)
        expiration = datetime.datetime.today() - datetime.timedelta(days=Log.log_expiration_days)

        #open log directory and for each file in there, 
        for filename in os.listdir(Log.log_dir):
            d = datetime.datetime.strptime(os.path.splitext(os.path.basename(filename))[0], '%Y-%m-%d')       #convert filename to a date to determine if it's older than the expiration date
            if d < expiration:                                  #if it is older then delete it
                os.remove(os.path.join(os.getcwd(), Log.log_dir, filename))

    @staticmethod
    def section_header(title, step_mode=False):
        global now
        now = Log.get_timestamp()
        
        print(Log.text_blue_on_black + title + "\n")

        if Log.enable_file_output:
            Log.write_to_file(title, "HEAD")

        if step_mode:
            input(Log.text_white_on_black + "...Press enter to continue...\n")

    @staticmethod
    def print(message):
        global now
        now = Log.get_timestamp()

        print(Log.text_gray_on_black + now + Log.text_white_on_black + " " + message)

        if Log.enable_file_output:
            Log.write_to_file(message, "INFO")

    @staticmethod
    def debug(message):
        global now
        now = Log.get_timestamp()

        if False:               #set this to True if you actually want debug statements to print to the console
            print(Log.text_gray_on_black + now + Log.text_white_on_black + " " + message)

        if Log.enable_file_output:
            Log.write_to_file(message, "DEBUG")

    @staticmethod
    def error(message):
        global now
        now = Log.get_timestamp()
        day = Log.get_date()

        print(Log.text_gray_on_black + now + Log.text_red_on_black + " " + message)

        if Log.enable_file_output:
            Log.write_to_file(message, "ERROR")

    @staticmethod
    def remove_colors(message):
        message = message.replace(Log.text_gray_on_black, "")
        message = message.replace(Log.text_red_on_black, "")
        message = message.replace(Log.text_green_on_black, "")
        message = message.replace(Log.text_orange_on_black, "")
        message = message.replace(Log.text_blue_on_black, "")
        message = message.replace(Log.text_purple_on_black, "")
        message = message.replace(Log.text_white_on_black, "")
        return message