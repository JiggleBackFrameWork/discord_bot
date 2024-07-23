import asyncio
import os

import random

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import Button, View

import colors
import servers_settings

from embededMessage import EmbededMessages


async def send_message(interaction, message, is_private=False):
    # Function code here

    await interaction.author.send(embed=message) if is_private else await interaction.channel.send(embed=message)


async def send_is_connected_error(interaction):
    await interaction.channel.send("The bot is currently playing audio, please wait until audio finishes")


directory = 'D:/Sound Board/discord/'
cringe_directory = 'D:/CodingDev/Python/discord_bot/cringe/'
ffmpeg_executable = "D:/CodingDev/Python/discord_bot/FFMPEG/ffmpeg.exe"
PLAY_SOUND_RANDOM_MAX = '16'

intents = discord.Intents.default()
intents.message_content = True

bot_prefix = '!'

bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

settings = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.after_invoke
async def testBoiii(ctx):
    print("This is a thing")


@bot.before_invoke
async def ensure_server_check(ctx):
    guild_id = ctx.guild.id
    if guild_id not in settings:
        await server_check_exists(ctx.guild)


@bot.command(name='list', aliases=['listing'])
async def test(ctx, *args):
    message = ctx.message.content[1:]

    if message == 'list':
        await ctx.send("He HE HA HA")
    elif message == 'listing':
        await ctx.send("Grrrrr")

    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}\n')


@bot.command(name='hello', aliases=['howdy', 'sup', 'wasgood', 'greetings!', "good'ay"])
async def greetings(ctx):
    return_message: Embed = discord.Embed(
        description="Howdy",
        color=colors.yellow
    )
    await ctx.send(embed=return_message)


@bot.command(name="check12")
async def check(ctx):
    guild_id = ctx.author.guild.id

    return_message: Embed = discord.Embed(
        description=settings[guild_id].audio_engine.is_playing,
        color=colors.yellow
    )
    await ctx.send(embed=return_message)


@bot.command(name="lenny", aliases=["restart", "cobain", "kurt"])
async def kms(ctx, *args):
    message = ctx.message.content[1:]
    description = ""

    if message == 'restart':
        description = "He HE HA HA"
    elif message == 'cobain':
        description = "Grrrrr"
    elif message == 'kurt':
        description = "Buurrrnn how I burrrnnnn"
    elif message == 'lenny':
        description = 'Tell me about the rabbits George'
    return_message: Embed = discord.Embed(
        description=description,
        color=colors.yellow
    )
    await ctx.send(embed=return_message)
    # RESTART FEATURE ADD HERE!!!!
    await ctx.send("NEED TO ADD RESTART FEATURE")


@bot.command(name="getSettings")
async def getSettings(ctx):
    guild_id = ctx.author.guild

    if settings:

        server = settings[guild_id]
        print(ctx.author)
        print(server.setting_sudoer_list)
        if str(ctx.author) in server.setting_sudoer_list:
            return_message: Embed = discord.Embed(
                description=str(server.get_setting()),
                color=colors.ceruleanblue
            )
            await ctx.send(embed=return_message)
        else:
            return_message: Embed = discord.Embed(
                description="You're not a sudoer, contact your server's admin for JiggleBack's server settings",
                color=colors.red
            )
            await ctx.send(embed=return_message)
    else:
        return_message: Embed = discord.Embed(
            description="There are no Servers Currently",
            color=colors.ceruleanblue
        )
        await ctx.send(embed=return_message)


@bot.command(name="addAnnoyable")
async def addAnnoyable(ctx, *args):
    p_message = str(args[0])
    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    server = settings[guild_id]
    if ctx.author in server.setting_sudoer_list:
        return_message: Embed = discord.Embed(
            description=f"Successfully added user {p_message}",
            color=colors.ceruleanblue
        )
        await ctx.send(embed=return_message)
    else:
        return_message: Embed = discord.Embed(
            description="You're not a sudoer, contact your server's admin for JiggleBack's server settings",
            color=colors.red
        )
        await ctx.send(embed=return_message)


@bot.command(name="jiffy")
async def jiffy(ctx, *arg):
    p_message = arg

    pp_message = ""

    for word in list(p_message):
        temp_list = list(word)
        letter = temp_list[0]
        if letter.isalpha():
            if letter.isupper():
                letter = 'J'
            else:
                letter = 'j'

        pp_message = pp_message + " " + word[0:].replace(word[0], letter, 1)

    return_message: Embed = discord.Embed(
        description=pp_message,
        color=colors.mediumpurple
    )
    await ctx.send(embed=return_message)


@bot.command(name='roll', aliases=['r'])
async def roll_die(ctx, *args):
    # Default values
    sides = 6
    times = 1

    # Parse arguments
    for arg in args:
        if arg.startswith('-d'):
            try:
                sides = int(arg[2:])
            except ValueError:
                await ctx.send("Invalid number of sides provided. Using default 6-sided die.")
                sides = 6
        elif arg.startswith('-t'):
            try:
                times = int(arg[2:])
            except ValueError:
                await ctx.send("Invalid number of rolls provided. Rolling 1 time.")
                times = 1

    # Roll the dice
    results = [random.randint(1, sides) for _ in range(times)]
    results_str = ', '.join(map(str, results))

    # Check if the result string is too long for a single embed
    max_embed_size = 6000
    if len(results_str) > max_embed_size:
        await ctx.send("The result is too long to display in a single message.")
        return

    return_message: Embed = discord.Embed(
        title="Dice Roll",
        description=f"Rolling a {sides}-sided die {times} time(s):\n{results_str}",
        color=colors.blue
    )

    try:
        await ctx.send(embed=return_message)
    except discord.HTTPException as e:
        return_message: Embed = discord.Embed(
            title="INVALID LENGTH",
            description=f"Failed to send message: {str(e)}",
            color=colors.outrageousorange
        )
        await ctx.send(embed=return_message)


@bot.command(name='p', aliases=['play'])
async def play_music(ctx, *args):
    url = ""
    if args[0] == "test":
        if int(args[1]) == 1:
            url = "https://www.youtube.com/watch?v=zAnQg7uFQCI"
        elif int(args[1]) == 2:
            url = "https://open.spotify.com/track/2aibwv5hGXSgw7Yru8IYTO?si=db509e65421e4d91"
        else:
            return_message: Embed = discord.Embed(
                description="That isn't an option... Do '1' for YT test, and '2' for spotify test.",
                color=colors.maroon
            )
            await ctx.send(embed=return_message)
            return
    else:
        url = args[0]

    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    results = await settings[guild_id].audio_cog.play(url, ctx)
    # description = "Audio Test"
    # color = colors.burlywood
    # if results[1] is not True:
    #     color = colors.maroon
    #     description = results[0]
    #
    # return_message: Embed = discord.Embed(
    #     description=description,
    #     color=color
    # )
    #
    # await ctx.send(embed=return_message)


@bot.command(name='stop', aliases=['disconnect'])
async def stop(ctx, *args):
    print("Stop")
    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id
    result = settings[guild_id].audio_cog.is_connected
    print(result)

    if result:
        await settings[guild_id].audio_cog.stop()
        return_message: Embed = discord.Embed(
            description="Disconnecting JiggleBack",
            color=colors.green)

    else:
        return_message: Embed = discord.Embed(
            description="Uhhhh did you mean that?",
            color=colors.firebrick)

    await ctx.send(embed=return_message)


@bot.command(name="s", aliases=['skip'])
async def skip(ctx):
    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    print("trying to skip")
    result = await settings[guild_id].audio_cog.skip()
    return_message: Embed = discord.Embed(
        description=result,
        color=colors.ceruleanblue
    )
    await ctx.send(embed=return_message)


@bot.command(name="pause", aliases=['resume'])
async def pause(ctx):
    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    print("Trying to pause")
    result = await settings[guild_id].audio_cog.pause()
    return_message: Embed = discord.Embed(
        description=result[0],
        color=result[1]
    )
    await ctx.send(embed=return_message)


@bot.command(name="radon")
async def radon(ctx, *args):
    if (len(args) != 1) and (args[0] != "sound"):
        return

    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id
    results = await settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=gXQkGSO9kH0",
                                                      ctx)
    description = "Beep"
    color = colors.cherenkovblue
    if results[1] is not True:
        description = results[0]

    return_message: Embed = discord.Embed(
        description=description,
        color=color
    )

    await ctx.send(embed=return_message)


@bot.command()
async def radio(ctx):
    '''
    if ctx.author.voice is None:
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    '''

    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    print("Running radio")
    file_path = "radio.txt"
    buttons = read_info_text_from_file(file_path)

    for button in buttons:
        button.set_cog(settings[guild_id].audio_cog)
        button.set_interaction(ctx)

    view = View()

    for button in buttons:
        view.add_item(button.button)

    message: Embed = discord.Embed(
        description="Pick a radio:",
        color=colors.cadetblue
    )
    await ctx.channel.send(embed=message, view=view)

    for button in buttons:
        button.button.callback = button.button_callback


@bot.command(name="missile?")
async def missile_knows(ctx):
    return_message: Embed = discord.Embed(
        description="The Missile Knows",
        color=colors.peru)
    await ctx.send(embed=return_message)
    await settings[ctx].audio_cog.play("https://www.youtube.com/watch?v=bZe5J8SVCYQ", ctx,
                                       send_message=False)


@bot.command(name="cringe", aliases=["cringe++", "cringe#"])
async def cringe(ctx):
    guild_id = None
    if ctx.guild is not None:
        guild_id = ctx.guild.id

    message = ctx.message.content[1:]
    description = ""

    if message == 'cringe':
        description = "Oh no CRINGE"
        return_message: Embed = discord.Embed(
            description=description,
            color=colors.cringe
        )
        await ctx.send(embed=return_message)

        await settings[guild_id].audio_cog.play_random_sound(ctx, cringe_directory,
                                                             ffmpeg_executable, PLAY_SOUND_RANDOM_MAX)


    elif message == 'cringe++':
        description = "Be Prepared"
        return_message: Embed = discord.Embed(
            description=description,
            color=colors.cringe
        )
        await ctx.send(embed=return_message)
        await settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=XvR3_U6xnts", ctx,
                                                send_message=False)
    elif message == 'cringe#':
        description = "I'm sorry little one"
        return_message: Embed = discord.Embed(
            description=description,
            color=colors.cringe
        )
        await ctx.send(embed=return_message)
        await settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=XvR3_U6xnts", ctx,
                                                send_message=False)
        await settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=7C1XtneJ1ok", ctx,
                                                send_message=False)


def read_info_text_from_file(file_path):
    embeded = []
    with open(file_path, 'r', encoding='utf-8') as file:
        i = 0
        for line in file:
            current_line = line
            title = current_line.split('title="')[1].split('" description=')[0]
            description = current_line.split('description="')[1].split('" url=')[0]
            url = current_line.split(" url='")[1].split("' color=")[0]
            color = current_line.split("color=")[1]
            embeded.append(EmbededMessages(title, description, url, color))
            i = i + 1

    return embeded


async def server_check_exists(guild):
    print("Server Check Exists!")
    # servers_settings.read_settings_from_file()
    # servers_settings.print_settings()
    if guild.id not in settings:
        print(f"Adding guild {guild.id} to settings")
        settings[guild.id] = servers_settings.Server_Settings(guild)
        await settings[guild.id].on_init(guild)
        print(f"Guild {guild.id} added to settings")


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:  # Check if the member is the bot
        return

    guild_id = member.guild.id
    await server_check_exists(member.guild)

    print("We are here 1 ")
    if (after.channel is not None) and (before.channel is None):
        print("We are here2")
        for user in settings[guild_id].annoyable:

            if user.annoyable.annoyable_user:
                print("We are here3")
                userid = member.id

                if user.annoyable.annoyable_text and settings[guild_id].server_annoyable_text:
                    print("We are here4")
                    user = await bot.fetch_user(userid)
                    await user.send(get_random_greeting())

                if user.annoyable.annoyable_voice and settings[guild_id].server_annoyable_voice:
                    print("We are here5")
                    files = os.listdir(directory)
                    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

                    if files:

                        track = str(random.choice(files))

                        if not settings[guild_id].audio_cog.is_connected:

                            voice_channel = after.channel
                            voice = await voice_channel.connect()
                            settings[guild_id].audio_cog.is_connected = True

                        else:
                            voice = settings[guild_id].audio_cog.voice

                        voice.play(discord.FFmpegPCMAudio(directory + track, executable=ffmpeg_executable))

                        while voice.is_playing():
                            await asyncio.sleep(0.1)

                        if not voice.is_playing():
                            await voice.disconnect()
                            settings[guild_id].audio_cog.is_connected = False

                    else:
                        print("No audio files found in the directory.")

    # @bot.event
    # async def on_message(interaction):
    #
    #     if interaction.author == bot.user:
    #         return
    #     await server_check_exists(interaction.guild)
    #
    #     username = str(interaction.author)
    #     user_message = str(interaction.content)
    #     channel = str(interaction.channel)
    #     owner = str(interaction.channel.guild)
    #     # print({interaction.author.voice})
    #     print(owner)
    #     print(f'{username} said: "{user_message}" ({channel})')
    #
    #     if user_message.startswith('!'):
    #         user_message = user_message.rsplit('!')[1]
    #         interaction.content = user_message
    #
    #         if user_message[0] == '?':
    #             user_message = user_message.rsplit('?')[1]
    #             interaction.content = user_message
    #             await send_message(interaction, await resp.get_response(interaction), is_private=True)
    #
    #         elif user_message == '!restart' or user_message == '!lenny':
    #             if user_message == '!lenny':
    #                 await send_message(interaction, await resp.get_response(interaction))
    #                 await client_1.close()
    #
    #             print("HERERERERER")
    #             await restart(interaction)
    #
    #         else:
    #
    #             await send_message(interaction, await resp.get_response(interaction))
    #
    #     elif user_message.startswith('/'):
    #         print(user_message)
    #         await send_message(interaction, await resp.get_response(interaction))


def get_random_greeting():
    greetings_file = "uwu_greetings.txt"  # Replace with your file path
    with open(greetings_file, "r", encoding="utf-8") as file2:
        greetings = file2.readlines()
    file2.close()
    # Choose a random greeting
    random_greeting = random.choice(greetings)
    return random_greeting


async def restart(interaction):
    print(interaction.author.name)
    current_file = open("master_admins.txt")
    allowed_admin_user = current_file.readlines()
    current_file.close()
    for i in range(len(allowed_admin_user)):
        allowed_admin_user[i] = allowed_admin_user[i].strip('\n')

    author = interaction.author.name

    if author in allowed_admin_user:
        def check(message):
            return (
                    message.author == interaction.author
                    and isinstance(message.channel, discord.DMChannel)
            )

        try:
            # guild_id = interaction.author.guild.id
            await interaction.author.send("Enter the Password: ")
            password_message = await bot.wait_for("message", timeout=30,
                                                  check=check)  # You can adjust the timeout as needed

            # Check if the password is correct
            if password_message.content == "BREH":

                await interaction.channel.send("Password is correct. Restarting...")
                for guild in settings:
                    await settings[guild].audio_cog.clear_queue()

                await bot.close()
            else:
                await interaction.author.send("Incorrect password. Restart aborted.")
        except asyncio.TimeoutError:
            await interaction.author.send("You didn't provide a password in time. Restart aborted.")
    else:
        await interaction.author.send(f"{author} not found in list of sudoers")


async def server_check_sudoers(author, server):
    if author in server.setting_sudoer_list:
        return True
    else:
        return False


sudoers_file = "sudoers_list.txt"
with open(sudoers_file, 'r') as file:
    allowed_users = [line.strip() for line in file]
file.close()

TOKEN_FILE_1 = "TOKEN_1.txt"
with open(TOKEN_FILE_1, "r") as file:
    TOKEN_1 = file.readlines()
file.close()

bot.run(TOKEN_1[0])
