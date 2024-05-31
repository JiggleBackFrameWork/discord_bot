import asyncio
import os
import random

import discord
import audio_cog
import responses as resp
# from discord.ext import commands
import audio_cog

import servers_settings


async def send_message(interaction, message, is_private=False):
    # Function code here

    await interaction.author.send(embed=message) if is_private else await interaction.channel.send(embed=message)


async def send_is_connected_error(interaction):
    await interaction.channel.send("The bot is currently playing audio, please wait until audio finishes")


directory = 'D:/Sound Board/discord/'
cringe_directory = 'D:/CodingDev/Python/discordBot/cringe/'
ffmpeg_executable = "D:/CodingDev/Python/discordBot/FFMPEG/ffmpeg.exe"
PLAY_SOUND_RANDOM_MAX = '16'

settings = {}


def run_discord_bot(TOKEN_1):
    intents = discord.Intents.default()
    intents.message_content = True
    client_1 = discord.Client(intents=intents)
    sudoers_file = "sudoers_list.txt"  # Replace with your file path
    with open(sudoers_file, 'r') as file:
        allowed_users = [line.strip() for line in file]
    file.close()

    @client_1.event
    async def on_ready():
        print(f'{client_1.user} is now running!')

    @client_1.event
    async def on_voice_state_update(member, before, after):

        if member.id == client_1.user.id:  # Check if the member is the bot
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
                        user = await client_1.fetch_user(userid)
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

    @client_1.event
    async def on_message(interaction):

        if interaction.author == client_1.user:
            return
        await server_check_exists(interaction.guild)

        username = str(interaction.author)
        user_message = str(interaction.content)
        channel = str(interaction.channel)
        owner = str(interaction.channel.guild)
        # print({interaction.author.voice})
        print(owner)
        print(f'{username} said: "{user_message}" ({channel})')

        if user_message.startswith('!'):
            user_message = user_message.rsplit('!')[1]
            interaction.content = user_message

            if user_message[0] == '?':
                user_message = user_message.rsplit('?')[1]
                interaction.content = user_message
                await send_message(interaction, await resp.get_response(interaction), is_private=True)

            elif user_message == '!restart' or user_message == '!lenny':
                if user_message == '!lenny':

                    await send_message(interaction, await resp.get_response(interaction))
                    await client_1.close()

                print("HERERERERER")
                await restart(interaction)

            else:

                await send_message(interaction, await resp.get_response(interaction))

        elif user_message.startswith('/'):
            print(user_message)
            await send_message(interaction, await resp.get_response(interaction))

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
                password_message = await client_1.wait_for("message", timeout=30,
                                                           check=check)  # You can adjust the timeout as needed

                # Check if the password is correct
                if password_message.content == "BREH":

                    await interaction.channel.send("Password is correct. Restarting...")
                    for guild in settings:
                        await settings[guild].audio_cog.clear_queue()

                    await client_1.close()
                else:
                    await interaction.author.send("Incorrect password. Restart aborted.")
            except asyncio.TimeoutError:
                await interaction.author.send("You didn't provide a password in time. Restart aborted.")
        else:
            await interaction.author.send(f"{author} not found in list of sudoers")

    client_1.run(TOKEN_1)


async def server_check_exists(guild):
    guild_id = guild.id
    if guild_id not in settings:
        print(guild)
        settings[guild_id] = servers_settings.ServersSettings(guild)
        print(settings[guild_id].get_setting())

async def server_check_sudoers(author, server):

    if author in server.setting_sudoer_list:
        return True
    else:
        return False
