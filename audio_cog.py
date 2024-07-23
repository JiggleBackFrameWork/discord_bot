import asyncio
import html
import os
import random
import re

import discord
import requests
import yt_dlp
from discord import Embed

import colors


async def disappointed_responses(amount_o_times):
    file = open('disappointed_phrases.txt')

    # read the content of the file opened
    disappointed_phrases = file.readlines()
    file.close()
    range_boi = len(disappointed_phrases) - 1
    print("disappointed_phrases range ", range_boi)
    return disappointed_phrases[random.randint(0, range_boi)].format(amount_o_times)


async def pick_random_sound(directory):
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    print("files", files)
    if files:
        track = str(random.choice(files))
        return directory + track


class AudioCog:
    def __init__(self):

        self.voice = None
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'quiet': True,
        }
        self.FFMPEG_OPTIONS = {
            'options': '-vn',
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -analyzeduration 0 -loglevel panic'
        }
        self.is_connected = False
        self.vc = None
        self.guild = None
        self.FFMPEG_EXECUTABLE = "D:/RandomDownload/ffmpeg.exe"
        self.is_skipped = False

    def get_vc(self):
        return self.vc

    async def play_sound(self, interaction, audio, title, send_message):
        audio_source = discord.FFmpegPCMAudio(audio, executable=self.FFMPEG_EXECUTABLE, **self.FFMPEG_OPTIONS)
        if send_message:
            return_message = Embed(
                description=f"Now playing {title}",
                color=colors.green)
            await interaction.send(embed=return_message)

        self.voice.play(audio_source)

        self.music_queue.pop(0)
        while self.is_connected:
            while self.voice.is_playing() and not self.is_skipped:
                await asyncio.sleep(0.1)

            if self.is_paused and not self.voice.is_playing() and not self.is_skipped:
                while self.is_paused:
                    await asyncio.sleep(0.1)

            elif len(self.music_queue) == 0 and not self.is_paused and not self.voice.is_playing():
                self.is_connected = False
                self.is_playing = False
                print("ENDING")
                await self.voice.disconnect(force=True)
            elif (len(self.music_queue) > 0 and not self.is_paused and not self.voice.is_playing()) or self.is_skipped:
                if self.is_skipped:
                    self.is_skipped = False

                song = str(self.music_queue[0])

                if await check_if_spotify(song):
                    # ADD SPOT PLAYLIST HERE

                    artist, title, url, success = await get_yt_url(song)

                else:

                    url, title, success = await self.find_url(song)

                if success:
                    audio_source = discord.FFmpegPCMAudio(url, executable=self.FFMPEG_EXECUTABLE,
                                                          **self.FFMPEG_OPTIONS)
                if send_message:
                    return_message = Embed(
                        description=f"Now playing {title}",
                        color=colors.green)
                    await interaction.send(embed=return_message)

                self.voice.play(audio_source)
                self.music_queue.pop(0)

    async def find_url(self, query):
        with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info_dict = ydl.extract_info(query, download=False)
                video_title = info_dict.get('title', None)
                return info_dict['url'], video_title, True
            except Exception as e:
                print(e)
                return "", "", False

    async def play_music(self, interaction, send_message):
        if len(self.music_queue) > 0:
            self.is_playing = True
            song_url = str(self.music_queue[0])

            if await check_if_spotify(song_url):

                artist, title, url, success = await get_yt_url(song_url)

            else:
                url, title, success = await self.find_url(song_url)

            if not self.is_connected:
                self.voice = await self.vc.connect()
                self.is_connected = True
            print(f"\n\nThis is the URL: {url}\nThis is the song: {title}")
            await self.play_sound(interaction, url, title, send_message)

            if success is not True:
                message = f"I'm sorry, I cant find anything with the url: {song_url}. Are you sure you typed that right?"
                color = colors.pantone448C
                return_message = Embed(
                    description=message,
                    color=color)
                await interaction.send(embed=return_message)

        else:
            self.is_playing = False
            self.is_connected = False
            await self.voice.disconnect(force=True)

    async def play(self, query, interaction, send_message=True):
        try:
            self.vc = interaction.author.voice.channel
        except Exception:
            self.vc = None

        if self.vc is None:
            return ["Connect to a voice channel!", False]

        elif self.is_paused:
            self.vc.resume()
            self.music_queue.append(query)

        elif self.is_playing:
            self.music_queue.append(query)
            print(self.music_queue)
        else:
            # $ ADD STUFF HERE
            if "open.spotify.com/playlist/" in query:
                print("Is a playlist")
                match = re.search(r'playlist/(\w+)', query)
                r = requests.get(query)
                content = r.content.decode('utf-8')  # Decode content as UTF-8
                pattern = r'content="https://open.spotify.com/track/(\w+)"'
                matches = re.findall(pattern, content)

                print(f"matches {match}")
                print(f"pattern {pattern}")
                print(f"matches {matches}")
                for track_id in matches:
                    track_url = "https://open.spotify.com/track/" + track_id
                    self.music_queue.append(track_url)

            elif "youtube.com/playlist" in query or "&list=" in query:
                print("YouTube Playlist")
                if "&index" in query:
                    query = re.sub(r'&index=\d+', '', query)
                ydl_opts = {
                    'quiet': True,
                    'extract_flat': 'in_playlist',  # Extracts only metadata, no downloading
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(query, download=False)
                    if 'entries' in info:
                        # The link is a playlist
                        print("Is YT playlist")
                        print(f"Playlist Title: {info['title']}")
                        for entry in info['entries']:
                            print(
                                f"Video Title: {entry['title']}, URL: https://www.youtube.com/watch?v={entry['id']}")
                            self.music_queue.append(f"https://www.youtube.com/watch?v={entry['id']}")
                    else:
                        # The link is a single video
                        print(f"Single Video Title: {info['title']}, URL: {query}")
                        self.music_queue.append(query)
            else:
                self.music_queue.append(query)
            print(self.music_queue)
            return await self.play_music(interaction, send_message)

    async def pause(self):
        if self.is_playing:
            if not self.is_paused:
                self.is_paused = True
                self.voice.pause()
                print("music paused")
                return ["Music paused", colors.red]
            elif self.is_paused:
                self.is_paused = False
                self.voice.resume()
                print("music resumed")
                return ["Music resumed", colors.green]
        else:
            return ["Uhhhhhhhh Re think broski", colors.lime]

    async def resume(self):
        if self.is_paused:
            self.is_paused = False
            self.voice.resume()

    async def skip(self) -> str:
        print("SKIPPING")
        if self.is_playing and not self.is_paused:
            self.is_skipped = True
            self.voice.pause()
            print(self.music_queue)
            return "Skipped"
        elif self.is_paused:
            return "Bro...."
        else:
            return "Why?"

    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if i > 4:
                break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    async def clear_queue(self):
        self.music_queue = []

    async def stop(self):
        self.is_playing = False
        self.is_paused = False
        self.is_connected = False
        await self.clear_queue()
        await self.voice.disconnect()

    async def play_greeting(self):
        self.voice.play(discord.FFmpegPCMAudio("StartUpGreeting.wav", executable=self.FFMPEG_EXECUTABLE))
        while self.voice.is_playing():
            await asyncio.sleep(0.1)

    async def play_random_sound(self, interaction, directory, ffmpeg_executable, PLAY_SOUND_RANDOM_MAX):
        user_message = str(interaction.message.content)
        username = str(interaction.author)

        try:
            print("CHECKING RANDOM")
            self.vc = interaction.author.voice.channel
        except Exception:
            self.vc = None

        if self.vc is None:
            return_message = discord.Embed(
                description="Connect to a voice channel!",
                color=colors.cringe
            )
            await interaction.send(embed=return_message)
            return

        if user_message == "random sound":
            return_message = discord.Embed(
                description="Playing Random Sound",
                color=colors.burlywood
            )
            self.voice = await self.vc.connect()
            await interaction.send(embed=return_message)
            self.voice.play(
                discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
            while self.voice.is_playing():
                await asyncio.sleep(0.1)

            if not self.voice.is_playing():
                await self.voice.disconnect()
            return

        print(user_message)
        amount_o_times = user_message.rsplit('x')[1]

        annoyable = "annoyable.txt"  # Replace with your file path
        with open(annoyable, 'r') as file:
            annoyable = [line.strip() for line in file]
        file.close()

        if amount_o_times.isdigit():
            if int(amount_o_times) < int(PLAY_SOUND_RANDOM_MAX):
                return_message = Embed(
                    description=f'Playing for {amount_o_times} times',
                    color=colors.peru)
                await interaction.send(embed=return_message)
                self.voice = await self.vc.connect()
                for x in range(int(amount_o_times)):
                    self.voice.play(
                        discord.FFmpegPCMAudio(await pick_random_sound(directory), executable=ffmpeg_executable))
                    while self.voice.is_playing():
                        await asyncio.sleep(0.1)
                await self.voice.disconnect(force=True)
            elif (int(amount_o_times) >= int(PLAY_SOUND_RANDOM_MAX)) and (username in annoyable):
                for x in range(int(amount_o_times)):
                    await interaction.author.send(await disappointed_responses(amount_o_times))
            else:
                await interaction.channel.send(await disappointed_responses(amount_o_times))


async def check_if_spotify(url):
    spotify_url = "open.spotify.com"
    if spotify_url in url:
        return True
    else:
        return False


async def get_yt_url(spotify_url):
    title, artist = get_spotify_info(spotify_url)
    query = f"{title} by {artist}"
    url = find_best_url(query)
    return artist, title, url, True


def get_spotify_info(url):
    # Extract the Spotify track ID from the URL
    match = re.search(r'track/(\w+)', url)
    if not match:
        print("Invalid Spotify URL. Please provide a valid track URL.")
        return

    r = requests.get(url)

    # print content of request
    content = r.content

    # Use regular expressions to extract the title and artist
    title_match = re.search(r'<title>(.*?) - song and lyrics by (.*?) \| Spotify</title>', str(content))

    if title_match:
        print(title_match.group(1))
        title = decode_html_sequence_strong(title_match.group(1))
        artist = decode_html_sequence_strong(title_match.group(2))
        print("Title:", title)
        print("Artist:", artist)
        return title, artist
    else:
        return


def decode_html_sequence_strong(html_sequence):
    # Adds an html wrapper
    decoded_string = html.unescape(decode_html_sequence(html_sequence))

    return decoded_string


def decode_html_sequence(html_sequence):
    # Regular expression to find all hexadecimal sequences in the format \xHH
    hex_pattern = re.compile(r'\\x([0-9A-Fa-f]{2})')

    # Initialize the decoded string and a list to collect byte values
    byte_values = []
    last_pos = 0
    decoded_string = ''

    # Iterate through all matches of the pattern
    for match in hex_pattern.finditer(html_sequence):
        # Append the substring before the current match
        decoded_string += html_sequence[last_pos:match.start()]

        # Collect the hex value to the byte_values list
        hex_value = match.group(1)
        byte_values.append(hex_value)

        # Update the last position
        last_pos = match.end()

        # If not at the end, decode the collected bytes and reset byte_values
        if last_pos < len(html_sequence) and not hex_pattern.match(html_sequence[last_pos:last_pos + 4]):
            hex_string = ''.join(byte_values)
            bytes_obj = bytes.fromhex(hex_string)
            decoded_string += bytes_obj.decode('utf-8')
            byte_values = []

    # Append any remaining part of the string and decode remaining collected bytes
    decoded_string += html_sequence[last_pos:]
    if byte_values:
        hex_string = ''.join(byte_values)
        bytes_obj = bytes.fromhex(hex_string)
        decoded_string = decoded_string.replace(hex_pattern.pattern, '')  # Remove the hex pattern
        decoded_string += bytes_obj.decode('utf-8')

    return decoded_string


def find_best_url(query):
    # Create YouTube-DL options
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',
        'default_search': 'ytsearch'
    }

    # Search for the best URL
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Query {query}")
        try:
            info = ydl.extract_info(query, download=False)
            print(f"Query2 {query}")

            if 'entries' in info and info['entries']:
                video = info['entries'][0]
            else:
                video = info

            # Get the best URL
            best_url = video['url']
            print("Best URL:", best_url)
            return best_url

        except Exception as e:
            print(f"Error extracting info: {e}")
            return None


def decode_utf8_string(utf8_string):
    try:
        print("decoding")
        decoded_string = utf8_string.encode('latin1').decode('utf-8')
    except UnicodeDecodeError:
        decoded_string = utf8_string
    return decoded_string
