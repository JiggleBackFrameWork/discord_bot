'''
This is for Server Viewing - Should View different aspects of
server life ie things like leaving and joining vc
Make sure implement every feature with a settings aspect too
'''

import bot


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')