# main.py
import os
import sys

# Replace 'bot.py' with the filename of your bot script
BOT_SCRIPT = 'bot.py'

# Run the bot
if __name__ == '__main__':
    try:
        while True:
            os.system(f'python {BOT_SCRIPT}')
    except KeyboardInterrupt:
        sys.exit(0)
