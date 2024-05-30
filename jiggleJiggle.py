import bot
# from discord.ext import commands


TOKEN_FILE_1 = "TOKEN_1.txt"  # Replace with your file path
with open(TOKEN_FILE_1, "r") as file:
    TOKEN_1 = file.readlines()
file.close()

bot.run_discord_bot(TOKEN_1[0])
