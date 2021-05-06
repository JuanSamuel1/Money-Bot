import discord
import os
from replit import db
import random 
import asyncio
from keep_alive import keep_alive

intents = discord.Intents.all()

def create_leaderboard(sorted_name,sorted_score):
  leaderboard= '''
  \nRank         Name               Balance\n'''
  for i in range(len(sorted_name)):
    leaderboard += "#"+str(i+1)+"\t"+str(sorted_name[i])+"    "+str(sorted_score[i])+"\n"
  return leaderboard

client = discord.Client(intents=intents)
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  msg = message.content
  if message.author == client.user:
    return
  
  if msg.startswith(";info"):
    info_message = '''
    Welcome to Money BOT!\
    \nA simple bot to play with your friends!\
    \n\
    \nHere is some information about this bot:\
    \n1) ;init \
       \nType this single word and your account is settled, Get $1000 as your first balance! \
    \n\
    \n2) ;info \
       \nYou'll get all the information you need to get start with this BOT! \
    \n\
    \n3) ;balance \
       \nDon't get carried away! Always check your balance before betting! \
    \n\
    \n4) ;coin [HEAD/TAIL] [AMOUNT_BET] \
       \nStart with a classic head or tail coin game! You'll get the amount you bet if you win! \
    \n\
    \n5) ;card [AMOUNT_BET]\
       \nType this word and a card will be picked randomly from a deck, type LOWER or HIGHER or EQUAL!\
    You'll get the amount you bet if you guess correctly, but if you guess equal , you'll get 10x \
       amount you bet. Be a king of gambler and guess EQUAL! \
    \n\
    \n6) ;donate [RECIPIENT] [AMOUNT_BET] \
       \nBe generous and give your friend in need! I'm sure your friend will pay you back soon!\
    \n\
    \n7) ;rank\
       \nDisplay your rank compared with your friend in one server! Race until you be the king of the hill!\
    \n\
    \n8) ;reset\
       \nTo desperate with your balance? That's why you don't gamble with real money! We provide you with\
  a simple option to delete your account and you can make a new one with $1000 as your first balance!\
    \n\
    \nHave fun playing this game with your friends!
    '''
    await message.channel.send(info_message)

  if msg.startswith(";init"):
    if(message.author.name not in db.keys()):
      db[message.author.name] = 1000
      embed = discord.Embed(color = discord.Colour.green(), description="Yay! you have $1000 in your balance now")
      embed.set_author(name='Welcome!', icon_url= message.author.avatar_url)
      await message.channel.send(embed=embed)
    else:
      await message.channel.send("You have created your balance")

  if msg.startswith(";daily"):
    embed = discord.Embed(color = discord.Colour.green(), description="Sorry,the coin landed on tails.")
    embed.set_author(name='Tails !', icon_url= message.author.avatar_url)
    await message.channel.send(embed=embed)

  if msg.startswith(";balance"):
    balance = db[message.author.name]
    embed = discord.Embed(color = discord.Colour.green(), description="Your balance is $"+str(balance))
    embed.set_author(name='Balance', icon_url= message.author.avatar_url)
    await message.channel.send(embed=embed)
  
  if msg.startswith(";coin"):
    content = msg.split(' ')
    coin_dict = {1:['HEAD','HEADS'], 2:['TAIL','TAILS']}
    flipped_coin = coin_dict[random.randint(1,2)]
    if(db[message.author.name] >= int(content[2])):
      if(content[1].upper() in flipped_coin):
        db[message.author.name] += int(content[2])
        embed = discord.Embed(color = discord.Colour.green(), description="Congratulations! The coin landed on "+content[1].upper()+'.')
        embed.set_author(name=content[1].upper()+' !', icon_url= message.author.avatar_url)
        embed.set_footer(text= "You've won $"+content[2])
        await message.channel.send(embed=embed)
        
      else:
        db[message.author.name] -= int(content[2])
        embed = discord.Embed(color = discord.Colour.green(), description="Sorry,the coin landed on "+flipped_coin[1].upper())
        embed.set_author(name=flipped_coin[1].upper()+' !', icon_url= message.author.avatar_url)
        await message.channel.send(embed=embed)
    else:
      await message.channel.send("You have insufficient balance to bet!") 

  if msg.startswith(";card"):
    symbol =['Clubs','Spades','Diamonds','Hearts']
    card_dict ={11:'Jack',12:'Queen',13:'King', 14:'Ace'}
    card_num = random.randint(2,14)
    card_symbol = random.choice(symbol)
    content = msg.split(' ')
    bet= content[1]
    if(int(bet) <= db[message.author.name]):
      if(card_num not in card_dict.keys()):
        card = str(card_num) + " of "+ card_symbol
      else:
        card = card_dict[card_num] + " of " + card_symbol
      embed = discord.Embed(color = discord.Colour.green(), description="The card drawn is "+card+"\nGo pick LOWER or HIGHER or EQUAL!")
      embed.set_author(name="BEEP BOOP!", icon_url= message.author.avatar_url)
      await message.channel.send(embed= embed)
      def check(m):
        return (m.content == "HIGHER" or m.content == "LOWER" or m.content == "EQUAL") and m.author == message.author
      try:
        answer = await client.wait_for('message', timeout=10.0, check=check)
      except asyncio.TimeoutError:
        await message.channel.send('Too Late! You lose your bet!')
        db[message.author.name] -= int(bet)
      else:
        new_card_num = random.randint(2,14)
        new_card_symbol = random.choice(symbol)
        if(new_card_num > card_num):
          conclusion = "HIGHER"
        elif(new_card_num == card_num):
          conclusion = "EQUAL"
        else:
          conclusion = "LOWER"
      
        if(new_card_num not in card_dict.keys()):
          new_card = str(new_card_num) + " of "+ new_card_symbol
        else:
          new_card = card_dict[new_card_num] + " of " + new_card_symbol
      
        new_card_text = "The next card drawn is "+new_card
        if(conclusion == answer.content):
          if(conclusion == "EQUAL"):
            embed = discord.Embed(color = discord.Colour.green(), description="Congratulation! "+new_card_text+"\nIt's EQUAL!")
            embed.set_author(name='EQUAL!', icon_url= message.author.avatar_url)
            embed.set_footer(text= "You've won $"+str(10*int(bet))+" 💰")
            db[message.author.name] += 10*int(bet)
          else:
            embed = discord.Embed(color = discord.Colour.green(), description="Congratulation! "+new_card_text+"\nIt's "+ conclusion+'!')
            embed.set_author(name=conclusion+'!', icon_url= message.author.avatar_url)
            embed.set_footer(text= "You\'ve won $"+str(0.5*int(bet))+" 💰")
            db[message.author.name] += 0.5*int(bet)
          await message.channel.send(embed=embed) 
        else:
          embed = discord.Embed(color = discord.Colour.green(), description="Sorry," +new_card_text+"\nIt's "+ conclusion+'!')
          embed.set_author(name=conclusion+'!', icon_url= message.author.avatar_url)
          await message.channel.send(embed=embed)
          db[message.author.name] -= int(bet)
    else:
      await message.channel.send("Insufficient balance!")

  if msg.startswith(";donate"):
    content = msg.split(' ')
    recipient = content[1]
    if(recipient not in db.keys()):
      await message.channel.send("Recipient hasn't had an account yet!\nMaybe you type the name wrongly?")
    else:
      if(int(content[2]) > db[message.author.name]):
        await message.channel.send("You have insufficient balance! ")
      else:
        db[message.author.name] -= int(content[2])
        db[recipient] += int(content[2])
        await message.channel.send("Successful!\n You have given "+recipient+" $"+str(content[2])+" 💰")
  
  if msg.startswith(";rank"):
    rank={}
    members =message.guild.members
    for member in members:
      print(member)
    for member in members:
      if(member.name in db.keys()):
        rank[member.name] = db[member.name]
    sorted_score = sorted(rank.values(),reverse=True)
    sorted_name = []
    for element in sorted_score:
      for k in rank.keys():
        if(rank[k] == element):
          sorted_name.append(k)
          break
    leaderboard = create_leaderboard(sorted_name,sorted_score)
    embed = discord.Embed(color = discord.Colour.green(), description=leaderboard)
    embed.set_author(name="LEADERBOARD 👑", icon_url= message.author.avatar_url)
    await message.channel.send(embed= embed)
      
  if msg.startswith(";reset"):
    if(message.author.name not in db.keys()):
      await message.channel.send("You haven't made an account!")
    else:
      embed = discord.Embed(color = discord.Colour.red(), description="Are you sure you want to delete your account?")
      embed.set_author(name='ALERT!!!', icon_url= message.author.avatar_url)
      await message.channel.send(embed=embed)
      def check(m):
        m_content = m.content.strip(' ')
        return (m_content.upper() == "YES" or m_content.upper() == "NO") and m.author == message.author
      try:
        answer = await client.wait_for('message', timeout=10.0, check=check)
      except asyncio.TimeoutError:
        await message.channel.send('You cancel the deletion of your account!')
      else:
        if answer.content.strip(' ').upper() == "NO":
          await message.channel.send('You cancel the deletion of your account!')
        else:
          del db[message.author.name]
          await message.channel.send("Your account have been deleted!")
    
  
keep_alive()
client.run(os.getenv('TOKEN'))