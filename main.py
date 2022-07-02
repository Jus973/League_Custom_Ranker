import discord
from discord.ext import commands
import os
from datetime import datetime
from PIL import Image
import pytesseract
from pinger import pinger

def elo_function(totalopp, totalteam, goldratio, kdaratio, win, ogs):
  ogscore = ogs
  if kdaratio == 0:
	  kdaratio=1
  if win:
    newscore = ogscore + (float(totalopp)/float(totalteam)) * 7 * float(goldratio) * float(kdaratio)
  else:
	  newscore=ogscore-(float(totalteam)/float(totalopp)) * 30 / float(goldratio) / float(kdaratio)
  return newscore
  
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
  print(bot.user.name)


@bot.command()
async def enter_result(ctx):
  if(ctx.author.id != 712697061773934592 and ctx.author.id != 542870634720395275 and ctx.author.id != 341406085460131851):
    await ctx.channel.send("You dont have permission to do that!")
    return
    
  await ctx.channel.send("Please enter everyone on the winning team with mentions:")

  msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
  winning_team = msg.mentions
  winkda=[]
  winratio=[]
  for x in range(len(winning_team)):
    winning_team[x]=winning_team[x].id
    await ctx.channel.send("Please enter KDA ratio of <@"+str(winning_team[x])+">")
    msg2 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    winkda.append(float(msg2.content))
    await ctx.channel.send("Please enter gold ratio of <@"+str(winning_team[x])+">")
    msg3 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    winratio.append(float(msg3.content))
		
    
  await ctx.channel.send("Please enter everyone on the losing team with mentions:")

  msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
  
  losing_team = msg.mentions
  losekda=[]
  loseratio=[]
  for x in range(len(losing_team)):
    losing_team[x]=losing_team[x].id
    await ctx.channel.send("Please enter KDA ratio of <@"+str(losing_team[x])+">")
    msg4 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    losekda.append(float(msg4.content))
    await ctx.channel.send("Please enter gold ratio of <@"+str(losing_team[x])+">")
    msg5 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    loseratio.append(float(msg5.content))

  with open('scores.txt','r') as f:
	  file=f.readlines()
			
  windices=[]
  losedices=[]
  winscores=[]
  losescores=[]
  wintotal=0
  losetotal=0
  print(file)
  for x in range(len(winning_team)):
	  for y in range(len(file)):
		  temp=file[y].split(' ')
		  if (int(winning_team[x])==int(temp[0])):
			  windices.append(y)
			  winscores.append(float(temp[1]))
			  wintotal=wintotal+winscores[x]
  for x in range(len(losing_team)):
	  for y in range(len(file)):
		  temp=file[y].split(' ')
		  if (int(losing_team[x])==int(temp[0])):
			  losedices.append(y)
			  losescores.append(float(temp[1]))
			  losetotal=losetotal+losescores[x]
  for x in range(len(winning_team)):
	  winscores[x]=elo_function(losetotal,wintotal,winratio[x],winkda[x],True,winscores[x])
  for x in range(len(losing_team)):
	  losescores[x]=elo_function(wintotal,losetotal,loseratio[x],losekda[x],False,losescores[x])
  for y in range(len(windices)):
	  x=int(windices[y])
	  temp=file[x].split(' ')
	  temp[1]=str(winscores[y])
	  temp=' '.join(temp)
	  file[x]=temp
  for y in range(len(losedices)):
	  x=int(losedices[y])
	  temp=file[x].split(' ')
	  temp[1]=str(losescores[y])
	  temp=' '.join(temp)
	  file[x]=temp
  print(file)
  with open('scores.txt','w') as f:
	  for x in (file):
		  f.write(str(x))
  await ctx.channel.send("Update successful: ")
  def keys(e):
	  return float(e[1])
  for y in range(len(file)):
	  file[y]=str(file[y]).split()
  file.sort(reverse=True,key=keys)
  for y in range(len(file)):
	  x=str(file[y]).split(' ')
	  x[2]=x[2].split("'#")[1]
	  x[2]=x[2].split("']")[0]
	  x[1]=x[1].split("'")[1]
	  await ctx.channel.send(str(y+1)+". "+x[2]+" score: "+x[1])

    

@bot.command()
async def custom_ranked(ctx):
  os.environ["TESSDATA_PREFIX"] = "wherever you put the Tessdata folder"
  pytesseract.pytesseract.tesseract_cmd = '/home/runner/Customs-Ranker/venv/bin/pytesseract.exe'
  
  fileName = str(ctx.author) + str(datetime.now())
  
  for attachment in ctx.message.attachments:
    await attachment.save(fileName + ".png")
  
  img = fileName + ".png"
  
  output = pytesseract.image_to_string(Image.open(img))
  print(output)
  


@bot.command()
async def hard_reset(ctx):
  if int(ctx.author.id)==542870634720395275 or int(ctx.author.id)==341406085460131851 or int(ctx.author.id)==712697061773934592:
    await ctx.channel.send("Are you sure?: (Y/N)")

    msg = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if("n" in msg.content.lower() or "N" in msg.content.lower()):
      return
    with open('scores.txt','r') as f:
      file=f.readlines()
    counter=0
    for x in file:
      x=x.split(' ')
      x[1]='1000'
      x=' '.join(x)
      file[counter]=x
      counter=counter+1
    with open('scores.txt','w') as f:
        for x in file:
          f.write(str(x))
    await ctx.channel.send("Reset successful, all scores are 1000")
  else:
    await ctx.channel.send("You dont have permission to do that!")
@bot.command()
async def leaderboard(ctx):
  with open('scores.txt','r') as f:
	    tempfile=f.readlines()
  await ctx.channel.send("Keep on climbing!!")
  def keys(e):
	  return float(e[1])
  for y in range(len(tempfile)):
	  tempfile[y]=str(tempfile[y]).split()
  tempfile.sort(reverse=True,key=keys)
  for y in range(len(tempfile)):
	  x=str(tempfile[y]).split(' ')
	  x[2]=x[2].split("'#")[1]
	  x[2]=x[2].split("']")[0]
	  x[1]=x[1].split("'")[1]
	  await ctx.channel.send(str(y+1)+". "+x[2]+" score: "+x[1])

pinger()
token = os.environ['TOKEN']
bot.run(token)
