from pickletools import float8
import discord
from discord.ext import commands
import os
from datetime import datetime
from PIL import Image
import pytesseract
from pinger import pinger

xd=True

def elo_function(totalopp, totalteam, goldratio, kdaratio, win, ogs):

  ogscore = ogs
  if kdaratio == 0:
      kdaratio=0.0000001
  
  if win:
    update=(float(totalopp) /float(totalteam)) * 7 * float(goldratio) * (kdaratio)
    if update>200:
      update=200
    newscore=ogscore+update
  else:
    update=(float(totalteam) /float(totalopp)) * 30 / float(goldratio) / float(kdaratio)
    if update>200:
       update=200
    newscore=ogscore-update
  if newscore<0:
     newscore=0
  return newscore

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
  print (bot.user.name)

@bot.command()
async def enter_result(ctx):
    if (ctx.author.id != 712697061773934592 and ctx.author.id != 542870634720395275 and ctx.author.id != 341406085460131851):
        await ctx.channel.send("You dont have permission to do that!")
        return
    
    await ctx.channel.send("Please enter everyone on the winning team with mentions:")

    msg = await bot.wait_for ("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
    
    winning_team = msg.mentions
    winkda = []
    winratio = []

    for x in range (len(winning_team)):
        
        winning_team[x] = winning_team[x].id
        await ctx.channel.send("Please enter KDA ratio of <@" + str(winning_team[x]) + ">")

        msg2 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        winkda.append(float(msg2.content))

        await ctx.channel.send("Please enter gold ratio of <@" + str(winning_team[x]) + ">")
        msg3 = await bot.wait_for("message", check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        winratio.append(float(msg3.content))
        

    await ctx.channel.send("Please enter everyone on the losing team with mentions:")

    msg = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)

    losing_team = msg.mentions
    losekda = []
    loseratio = []
    for x in range (len(losing_team)):

        losing_team[x] = losing_team[x].id
        await ctx.channel.send("Please enter KDA ratio of <@" + str(losing_team[x]) + ">")

        msg4 = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
        losekda.append(float(msg4.content))

        await ctx.channel.send("Please enter gold ratio of <@" + str(losing_team[x]) + ">")
        msg5 = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
        loseratio.append(float(msg5.content))

    with open('scores.txt','r') as f:
        file = f.readlines()
    
    windices = []
    losedices = []
    winscores = []
    losescores = []
    wintotal = 0 
    losetotal = 0
    print(file)

    for x in range(len(winning_team)):
        for y in range(len(file)):

            temp = file[y].split(' ')
            if (int(winning_team[x]) == int(temp[0])):
                windices.append(y)
                winscores.append(float(temp[1]))
                wintotal = wintotal + winscores[x]
    
    for x in range(len(losing_team)):
        for y in range(len(file)):

            temp = file[y].split(' ')
            if (int(losing_team[x]) == int(temp[0])):
                losedices.append(y)
                losescores.append(float(temp[1]))
                losetotal = losetotal + losescores[x]
    
    for x in range(len(winning_team)):
        winscores[x] = elo_function(losetotal, wintotal, winratio[x], winkda[x], True, winscores[x])
    
    for x in range(len(losing_team)):
        losescores[x] = elo_function(wintotal, losetotal, loseratio[x], losekda[x], False, losescores[x])

    for y in range(len(windices)):
        x = int(windices[y])
        temp = file[x].split(' ')
        temp[1] = str(winscores[y])
        temp = ' '.join(temp)
        file[x] = temp

    for y in range(len(losedices)):
        x = int(losedices[y])
        temp = file[x].split(' ')
        temp[1] = str(losescores[y])
        temp = ' '.join(temp)
        file[x] = temp
    

    with open('scores.txt','w') as f:
        for x in (file):
            f.write(str(x))
    
    await ctx.channel.send("Update successful: ")

    def keys(e):
        return float(e[1])
    
    for y in range(len(file)):
        file[y] = str(file[y]).split()
    
    file.sort(reverse = True, key = keys)
    returnStr = ""
    for y in range(len(file)):
        x = str(file[y]).split(' ')
        x[2] = x[2].split("'#")[1]
        x[2] = x[2].split("']")[0]
        x[1] = x[1].split("'")[1]
        returnStr += (str(y + 1) + ". " + x[2] + " score: " + x[1]+"\n")
    await ctx.channel.send(returnStr)
    

@bot.command()
async def custom_ranked(ctx):
  os.environ["TESSDATA_PREFIX"] = "/league_custom_ranker/tessdata"
  pytesseract.pytesseract.tesseract_cmd = '/home/runner/Customs-Ranker/venv/bin/pytesseract.exe'
  
  fileName = str(ctx.author) + str(datetime.now())
  
  for attachment in ctx.message.attachments:
    await attachment.save(fileName + ".png")
  
  img = fileName + ".png"
  
  output = pytesseract.image_to_string(Image.open(img))
  print(output)
  


@bot.command()
async def hard_reset(ctx):

    if int(ctx.author.id) == 542870634720395275 or int(ctx.author.id) == 341406085460131851 or int(ctx.author.id) == 712697061773934592:
        await ctx.channel.send("Are you sure?: (Y/N)")
        msg = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)

        if("n" in msg.content.lower() or "N" in msg.content.lower()):
            return

        with open('scores.txt','r') as f:
            file = f.readlines()
        
        counter=0
        
        for x in file:
            x = x.split(' ')
            x[1] = '1000'
            x = ' '.join(x)
            file[counter] = x
            counter = counter + 1
        
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
    
    tempfile.sort(reverse = True, key = keys)
    returnStr = ""
    for y in range(len(tempfile)):
        x = str(tempfile[y]).split(' ')
        x[2] = x[2].split("'#")[1]
        x[2] = x[2].split("']")[0]
        x[1] = x[1].split("'")[1]
        returnStr += (str(y + 1) + ". " + x[2] + " score: " + x[1] + "\n")
    await ctx.channel.send(returnStr)


@bot.command()
async def score(ctx):
  user = ctx.message.mentions[0].id
  with open('scores.txt','r') as f:
        tempfile=f.readlines()

        for y in range(len(tempfile)):
            tempfile[y] = str(tempfile[y]).split()
            if(str(tempfile[y][0]) == str(user)):
              await ctx.channel.send(tempfile[y][1])

@bot.command()
async def messenger(ctx):
  global xd
  if xd == True:
    await ctx.channel.send("Are you sure you want to turn autoresponder off? Y/N")
    msg = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
    
    if str(msg.content).lower() == "y":
      xd=False
      return
    else:
      return
  
  if xd == False:
    await ctx.channel.send("Are you sure you want to turn autoresponder on? Y/N")
    msg = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
    if str(msg.content).lower() == "y":
      xd=True
      return
    else:
      return
			
@bot.event
async def on_message(msg):
  global xd
  print("in #"+str(msg.channel)+": "+str(msg.author)+": "+str(msg.content))
  f = open("logs.txt", "a")
  f.write("in #"+str(msg.channel)+": "+str(msg.author)+": "+str(msg.content)+"\n")
  await bot.process_commands(msg)
  if xd == False:
    return
  if int(msg.author.id)==991939871948144720:
	  return
  if "oh nah" in msg.content.lower() and int(msg.author.id)==542870634720395275:
    await msg.channel.send(":skull:")
  if msg.content=="L" and int(msg.author.id)!=542870634720395275:
    await msg.channel.send("bozo")
  if msg.content.lower()=="ashley":
    await msg.channel.send("SHUT THE FUCK UP")
  if "kys" in msg.content.lower() or "kms" in msg.content.lower():
    await msg.channel.send("chill out bro it's not worth it")
  if "help me" in msg.content.lower():
    await msg.channel.send("Call 911 or text your loved ones or it's wraps")
  if "love" in msg.content.lower() or "so g" in msg.content.lower():
	  await msg.channel.send("stop dickriding bruh")
  if "cope" in msg.content.lower():
	  await msg.channel.send("copium")
  if "copium" in msg.content.lower():
	  await msg.channel.send("COPE BITCH")
  if "polo" in msg.content.lower():
	  await msg.channel.send("Caught him lackin in his whip, they still tryna find his face in there")
  if "pop out" in msg.content.lower():
	  await msg.channel.send("we pop out at your party, Im with the gang")
	

pinger()
token = os.environ['TOKEN']
bot.run(token)
