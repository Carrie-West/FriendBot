import os
import discord
from discord.ext import commands
import keepalive
import wikipedia
import pointbase
import random
import pandas as pd
import numpy as np

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/',intents=discord.Intents.all())

last_kisser = ''
multiplier = 1

@bot.command(pass_context = True)
async def summary(ctx,*,arg):
  results = wikipedia.search(arg)
  page = "'"+str(results[0])+"'"
  await ctx.send(wikipedia.summary(page)[:2000])

@bot.command(pass_context = True)
async def link(ctx,*,arg):
  results = wikipedia.search(arg)
  page = "'"+str(results[0])+"'"
  await ctx.send(wikipedia.page(page).url)
  
@bot.command(pass_context = True)
async def kiss(ctx):
  
  global multiplier
  global last_kisser
  
  kissable = random.randint(0,100)
  score = random.randint(1,100) * multiplier
  if (kissable >50):
    print(ctx.author)
    pointbase.points(str(ctx.author), score, ctx.author.id)
    num = pointbase.score(ctx.author.id)
    await ctx.send("mwah! " + str(score) + " points! (" + str(num) + " total)")
  else:
    pointbase.points(str(ctx.author), -score, ctx.author.id)
    num = pointbase.score(ctx.author.id)
    await ctx.send("Ew. I'll pass. " + str(-score) + " points. (" + str(num) + " total)")
  if (last_kisser == str(ctx.author)):
    multiplier = multiplier + 1
  else:
    last_kisser = str(ctx.author)
    multiplier = 1

@bot.command(pass_context = True)
async def slap(ctx, arg):
  
  global multiplier
  global last_kisser
  
  slapable = random.randint(0,100)
  score = random.randint(1,100) * multiplier
  try:
    if (slapable >50):
      pointbase.slap(str(arg), score)
      await ctx.send("Nah, they're cool! " + str(score) + " points to them!")
    
    else:
      pointbase.slap(str(arg), -score)
      await ctx.send("Yeah! Fuck you! " + str(-score) + " points.")
  except:
      await ctx.send("I don't know who you're talking about. Try again, loser.")
  if (last_kisser == str(ctx.author)):
    multiplier = multiplier + 1
  else:
    last_kisser = str(ctx.author)
    multiplier = 1

@bot.command(pass_context = True)
async def leaderboard(ctx):
  print(ctx.author.id)
  results = pointbase.leaderboard()
  board = pd.DataFrame(data=results)
  board.columns = ['Name', 'Points']
  board['Name'] = board['Name'].apply(lambda x: x[:-5].strip(''))
  board.index = board.index + 1
  print(board.to_string(justify='center'))
  board.style.set_properties(['Name'], **{'text-align': 'left'})
  board.style.set_properties(['Points'], **{'text-align': 'center'})

  await ctx.send("```"+ board.to_string(formatters={'Name':'{{:<{}s}}'.format(board['Name'].str.len().max()).format},justify='center') + "```")
keepalive.keep_alive()
bot.run(TOKEN)