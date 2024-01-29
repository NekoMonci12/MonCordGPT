import discord
from discord.ext import commands
from gtts import gTTS
import openai
from pytube import YouTube

# Configure OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Configure Discord Bot
bot_token = 'YOUR_DISCORD_BOT_TOKEN'
prefix = '!'

# Define intents
intents = discord.Intents.default()
intents.all()

# Create Bot instance with intents
bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='tts')
async def text_to_speech(ctx, *, text):
    tts = gTTS(text=text, lang='en')
    tts.save('tts.mp3')
    voice_channel = ctx.author.voice.channel
    voice_channel.play(discord.FFmpegPCMAudio('tts.mp3'))

@bot.command(name='openai')
async def openai_api(ctx, *, prompt):
    response = openai.Completion.create(
        engine='davinci',
        prompt=prompt,
        max_tokens=150
    )
    await ctx.send(response.choices[0].text)

@bot.command(name='avatar')
async def get_avatar(ctx, member: discord.Member):
    await ctx.send(member.avatar_url)

@bot.command(name='download')
async def download_media(ctx, url):
    yt = YouTube(url)
    ys = yt.streams.get_highest_resolution()
    ys.download('downloads')
    await ctx.send(f'Download complete: {ys.title}')

if __name__ == "__main__":
    bot.run(bot_token)
