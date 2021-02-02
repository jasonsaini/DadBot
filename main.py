import discord
import os
import requests
import json
from dadjokes import Dadjoke
from pyowm import OWM
from dotenv import load_dotenv

# Load tokens from .env
load_dotenv('token.env')

client = discord.Client()

# Initialize tokens 
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
owm = OWM(WEATHER_TOKEN)
mgr = owm.weather_manager()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
client.run(DISCORD_TOKEN)

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]['a']
  return quote

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  return

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  # Lowercase message for reading
  message.content = message.content.lower()

  #greets user
  if message.content.startswith('hello') or message.content.startswith('hi'):
    await message.channel.send("Hello!\nEnter \"help\" for information!")
    return
  
  #tells a random dad joke
  if 'joke' in message.content:
    dadjoke = Dadjoke()
    await message.channel.send(dadjoke.joke)
    return

  # tells "hi [], i'm dad" joke
  if (message.content.startswith('i\'m') or message.content.startswith('i am')):
    words = message.content.split(" ")
    words.pop(0)
    s = ' '.join(words)
    await message.channel.send(f"Hi {s.capitalize()}! I'm DadBot!")
    return
  
  # tells weather
  if 'weather' in message.content:
    location = " "
    words = message.content.split(" ")
    word_count = 0
    # Gets location from message
    for i in words:
      word_count += 1
      if i == "in":
        location = words[word_count]
        # Remove question mark from string
        if '?' in location:
          location = location[:-1]

  # Gets information from weather API      
    observation = mgr.weather_at_place(location)
    w = observation.weather
    weather = w.detailed_status
    temperature_dict = w.temperature('fahrenheit')
    temperature = temperature_dict.get("temp")
    location = location.capitalize()
    weather = weather.capitalize()
    await message.channel.send(f"{location} : {weather} and it's {temperature}\xb0F today!")
    return

  # Sends help information to user
  if "help" in message.content:
    await message.channel.send("Say hi to Your Dad Bot by saying Hi or Hello\nAsk for the weather. (Ex: What's the weather like in Orlando?)\nAsk me to tell a joke!\nAsk me for life advice/quotes!\nStart a sentence with \"I\'m\"")
    return

  # tells a random quote/advice
  if ("quote" or "advice" in message.content):
    quote = get_quote()
    await message.channel.send(quote)
    return
