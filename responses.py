import random
from discord.ui import Button, View
import discord
from discord import Embed

import bot
import colors
from audio_cog import AudioCog


async def get_response(interaction):
    try:
        p_message = str(interaction.content)
        print(p_message)

        guild_id = None
        server = None

        if interaction.guild is not None:
            guild_id = interaction.guild.id
            # Check if an audio_cog instance already exists for the guild

            server = bot.settings[guild_id]


        if p_message == 'hello':
            return_message: Embed = discord.Embed(
                description="Howdy",
                color=colors.yellow
            )
            return return_message

        elif "check12" in p_message:
            return_message: Embed = discord.Embed(
                description=bot.settings[guild_id].audio_cog.is_playing,
                color=colors.yellow
            )
            return return_message

        elif "lenny" in p_message:
            return_message: Embed = discord.Embed(
                description="Tell me about the rabbits George...",
                color=colors.yellow
            )
            return return_message

        elif "getSettings" in p_message:

            if bot.settings:

                server = bot.settings[guild_id]
                print(interaction.author)
                print(server.setting_sudoer_list)
                if str(interaction.author) in server.setting_sudoer_list:
                    return_message: Embed = discord.Embed(
                        description=str(server.get_setting()),
                        color=colors.ceruleanblue
                    )
                    return return_message
                else:
                    return_message: Embed = discord.Embed(
                        description="You're not a sudoer, contact your server's admin for JiggleBack's server settings",
                        color=colors.red
                    )
                    return return_message


            else:
                return_message: Embed = discord.Embed(
                    description="There are no Servers Currently",
                    color=colors.ceruleanblue
                )
                return return_message

        elif "addAnnoyable" in p_message:

            p_message = p_message.rsplit("addAnnoyable")[1]

            if interaction.author in server.setting_sudoer_list:
                return_message: Embed = discord.Embed(
                    description=f"Successfully added user {p_message}",
                    color=colors.ceruleanblue
                )
                return return_message
            else:
                return_message: Embed = discord.Embed(
                    description="You're not a sudoer, contact your server's admin for JiggleBack's server settings",
                    color=colors.red
                )
                return return_message


        elif "jiffy" in p_message:
            p_message = p_message.rsplit("jiffy")[1]
            p_message = p_message.split()
            pp_message = ""

            for word in list(p_message):
                temp_list = list(word)
                temp_list[0] = "j"

                pp_message = pp_message + " " + word[0:].replace(word[0], "j", 1)

            return_message: Embed = discord.Embed(
                description=pp_message,
                color=colors.mediumpurple
            )
            return return_message



        elif p_message == 'roll':

            return_message: Embed = discord.Embed(
                description="Rrrrrollling: {0}".format(str(random.randint(1, 6))),
                color=colors.mediumturquoise
            )
            return return_message

        elif p_message == '/help':
            all_commands = """ ```
All commands:
/help - displays all the available commands
/phelp - displays all the available Music commands

<Chat Commands>
!hello - says hi to the user
!jiffy - [Whatever words turned to "jords" that make up "jentences"]
!roll - Rolls a 1d6

<Random Commands>
!random sound [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
!radon sound - radon is among us
!cringe [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
!cringe++ - plays a 10 ish minute long cringe video
!cringe# - plays 2 10 ish minute long cringe videos
!missile? - describes where the missile is

<Music Bot Commands>
!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current 
    song if it was paused
!q - displays the current music queue
!skip - skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnected the bot from the voice channel
!pause - pauses the current song being played or resumes if already paused
!resume - resumes playing the current song
                ```
                """
            return_message: Embed = discord.Embed(
                description=all_commands,
                color=colors.green
            )
            return return_message

        elif p_message == '/phelp':
            music_commands = """ ```
Music commands:
!help - displays all Music Commands
!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current 
    song if it was paused
!q - displays the current music queue
!skip - skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnected the bot from the voice channel
!pause - pauses the current song being played or resumes if already paused
!resume - resumes playing the current song
               ```
               """
            return_message: Embed = discord.Embed(
                description=music_commands,
                color=colors.darkgreen
            )
            return return_message

        elif p_message == 'help':
            general_commands = """ ```
General commands:
/help - displays all the available commands
!random sound [xAMOUNT OF TIMES WANTED TO PLAY... Be nice]
!p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current
    song if it was paused
!q - displays the current music queue
!skip - skips the current song being played
!clear - Stops the music and clears the queue
!leave - Disconnected the bot from the voice channel
!pause - pauses the current song being played or resumes if already paused
!resume - resumes playing the current song
   ```
   """
            return_message: Embed = discord.Embed(
                description=general_commands,
                color=colors.lawngreen
            )
            return return_message

        elif "radio" == p_message:

            print("Running radio")
            file_path = "radio.txt"
            buttons = read_info_text_from_file(file_path)

            for button in buttons:
                button.set_cog(bot.settings[guild_id].audio_cog)
                button.set_interaction(interaction)

            view = View()

            for button in buttons:
                view.add_item(button.button)

            await interaction.channel.send("Pick a radio:", view=view)

            for button in buttons:
                button.button.callback = button.button_callback

        elif "skip" == p_message:
            print("trying to skip")
            result = await bot.settings[guild_id].audio_cog.skip()
            return_message: Embed = discord.Embed(
                description=result,
                color=colors.ceruleanblue
            )
            return return_message

        elif p_message == "pause" or p_message == "resume":
            print("Trying to pause")
            result = await bot.settings[guild_id].audio_cog.pause()
            return_message: Embed = discord.Embed(
                description=result[0],
                color=result[1]
            )
            return return_message


        elif 'p test' == p_message:
            results = await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=zAnQg7uFQCI",
                                                                  interaction)
            description = "Audio Test"
            color = colors.burlywood
            if results[1] is not True:
                color = colors.maroon
                description = results[0]

            return_message: Embed = discord.Embed(
                description=description,
                color=color
            )
            return return_message

        elif 'p test2' == p_message:
            results = await bot.settings[guild_id].audio_cog.play(
                "https://open.spotify.com/track/2aibwv5hGXSgw7Yru8IYTO?si=db509e65421e4d91", interaction)
            description = "Spaudio Test"
            color = colors.green
            if results[1] is not True:
                color = colors.maroon
                description = results[0]

            return_message: Embed = discord.Embed(
                description=description,
                color=color
            )
            return return_message

        elif "p " in p_message or "play" in p_message:
            url = p_message.split(" ")[1]
            results = await bot.settings[guild_id].audio_cog.play(url, interaction)
            if results[1] is not True:
                color = colors.maroon
                return_message: Embed = discord.Embed(
                    description=results[0],
                    color=color)
                return return_message

        elif "disconnect" == p_message or "stop" == p_message:
            print("Stop")
            result = bot.settings[guild_id].audio_cog.is_connected
            print(result)
            print(p_message)
            if result:
                await bot.settings[guild_id].audio_cog.stop()
                return_message: Embed = discord.Embed(
                    description="Disconnecting JiggleBack",
                    color=colors.green)
                return return_message
            else:
                return_message: Embed = discord.Embed(
                    description="Uhhhh did you mean that?",
                    color=colors.firebrick)
                return return_message

        elif "random sound" in p_message:
            await bot.settings[guild_id].audio_cog.play_random_sound(interaction, bot.directory, bot.ffmpeg_executable,
                                                                     bot.PLAY_SOUND_RANDOM_MAX)

        elif "radon sound" in p_message:
            results = await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=gXQkGSO9kH0",
                                                                  interaction)
            description = "Beep"
            color = colors.cherenkovblue
            if results[1] is not True:
                description = results[0]

            return_message: Embed = discord.Embed(
                description=description,
                color=color
            )
            return return_message

        elif "missile?" in p_message:
            return_message: Embed = discord.Embed(
                description="The Missile Knows",
                color=colors.peru)
            await bot.send_message(interaction, return_message)
            await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=bZe5J8SVCYQ", interaction,
                                                        send_message=False)



        elif "cringe++" in p_message:
            return_message = discord.Embed(
                description="Be Prepared",
                color=colors.cringe
            )
            await bot.send_message(interaction, return_message)
            await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=XvR3_U6xnts", interaction,
                                                        send_message=False)

        elif "cringe#" in p_message:
            return_message: Embed = discord.Embed(
                description="I'm sorry little one",
                color=colors.cringe
            )
            await bot.send_message(interaction, return_message)
            await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=XvR3_U6xnts", interaction,
                                                        send_message=False)
            await bot.settings[guild_id].audio_cog.play("https://www.youtube.com/watch?v=7C1XtneJ1ok", interaction,
                                                        send_message=False)


        elif "cringe" in p_message:
            await bot.settings[guild_id].audio_cog.play_random_sound(interaction, bot.cringe_directory,
                                                                     bot.ffmpeg_executable, bot.PLAY_SOUND_RANDOM_MAX)

        else:
            error_message: Embed = discord.Embed(
                description="Command not found. Type !/help for a list of all available commands",
                color=colors.outrageousorange)
            return error_message

    except Exception as e:
        print(f'{e} soooo error')


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


class EmbededMessages:

    def __init__(self, title, description, url, color):
        self.title = title
        self.description = description
        self.url = url
        self.color = int(color.split("\n")[0], 16)
        self.audio_cog = None
        self.interaction = None
        self.button = Button(label=self.description, style=discord.ButtonStyle.blurple, emoji="▶️")

    async def button_callback(self, button_interaction):
        embed = discord.Embed(title=self.title, description=self.description, url=self.url,
                              color=self.color)
        await button_interaction.response.send_message(embed=embed)
        await self.audio_cog.play(self.url, self.interaction)

    def set_cog(self, audio_cog):
        self.audio_cog = audio_cog

    def set_interaction(self, interaction):
        self.interaction = interaction
