import audio_cog


class Server_Settings:
    def __init__(self, guild):
        self.guild_id = guild.id
        self.audio_cog = audio_cog.AudioCog()
        self.server_annoyable_voice = False
        self.server_annoyable_text = False
        self.music_connect_start_sound = False
        self.setting_sudoer_list = [str(guild.owner), 'sir_zombieflambe']
        self.annoyable = []
        self.server_radios = {}
        self.guild_info = guild

    async def on_init(self, guild):
        # Initialize the settings for the server
        self.setting_sudoer_list = ["admin"]
        self.audio_cog = audio_cog.AudioCog()
        self.is_playing = False
        print(f"Initialized settings for guild {guild.id}")


    def get_setting(self):
        if self.guild_id is None:
            return "There are no guilds yet"
        else:
            return (f'Guild ID, {self.guild_id}\nGuild Name, {self.guild_info}\nAudio cog, {self.audio_cog}'
                    f'\nServer Annoy-able voice, {self.server_annoyable_voice}'
                    f'\nServer Annoy-able text, {self.server_annoyable_text}'
                    f'\nAnnoy-able users, {self.annoyable}'
                    f'\nConnect start sound, {self.music_connect_start_sound}'
                    f'\nServer sudoer\'s list, {self.setting_sudoer_list}'
                    f'\nServer radios, {self.server_radios}')



    async def addSudoer(self):
        print(",kld bhjsnfz")

    async def loadSetting(self, fileLocation):
        print("Loooaaaaaaaaaaaaaddd")

class Annoyable:

    def __init__(self, user):
        self.annoyable_user = user
        self.annoyable_voice = False
        self.annoyable_text = False