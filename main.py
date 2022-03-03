from keep_alive import keep_alive
import discord, asyncio, datetime, config
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_components import DiscordComponents, Button, ButtonStyle

bot = commands.Bot(
  command_prefix=config.PREFIX,
  description=config.DESCRIPTION,
  intents=discord.Intents.all(),
  help_command=None
)

DiscordComponents(bot)

############ NEW MODMAIL THREAD FUNCTION ############

async def newThread(message, chn, guild):
  await message.add_reaction("✅")
  log = bot.get_channel(config.LOG_CHANNEL)
  embed = discord.Embed(title="Thread created", description=f"**{message.author.mention} created a new thread!**", color=discord.Colour.green())
  embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  embed.set_footer(text=f"User ID: {message.author.id}")
  await log.send(embed=embed, components=[[Button(
            style=ButtonStyle.URL,
            label="View thread",
            url=f"https://discord.com/channels/{guild.id}/{chn.id}"
        )]])

  member = guild.get_member(int(message.author.id))
  roles = member.roles
  roles.reverse()
  joined_at = member.joined_at 
  since_created = (message.created_at - message.author.created_at).days
  if joined_at is not None:
      since_joined = (message.created_at - joined_at).days
      user_joined = joined_at.strftime("%d %b %Y %H:%M")
  else:
      since_joined = "?"
      user_joined = ("Unknown")
  user_created = member.created_at.strftime("%d %b %Y %H:%M")
  created_on = ("{}\n({} days ago)").format(user_created, since_created)
  joined_on = ("{}\n({} days ago)").format(user_joined, since_joined)

  embed = discord.Embed(title="New Thread", description=f"Type `!reply <message>` in this channel to reply to the thread.", color=discord.Colour.gold())
  embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  embed.add_field(name="User Mention", value=f"{message.author.mention}", inline=True)
  embed.add_field(name="User ID", value=f"{message.author.id}", inline=True)
  embed.add_field(name="Server Nickname", value=f"{member.display_name}", inline=True)
  embed.add_field(name="Account Creation", value=f"{created_on}", inline=True)
  embed.add_field(name="Join Server", value=f"{joined_on}", inline=True)
  embed.add_field(name="Highest Role", value=f"{roles[0].mention}", inline=True)
  await chn.send(embed=embed)

  creationEmbed = discord.Embed(title="Thread Created!", description=f"Thank you for reaching out to our community team, {message.author.mention}! Your message has been sent to our community team and they will get back to you via this bot! If you realise you no longer need help, please simply click the button below.", color=discord.Colour.gold())
  creationEmbed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
  creationEmbed.timestamp = datetime.datetime.utcnow()
  creationEmbed.set_footer(text=f"This is an automated message from {guild.name}")
  await message.author.send(embed=creationEmbed, components=[[Button(
        style=ButtonStyle.red,
        label="Close thread",
        custom_id="memberClose"
    )]])
  
  embed = discord.Embed(title="Incoming message", description=message.content, color=discord.Colour.green())
  embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  embed.set_footer(text=f"User ID: {message.author.id}")
      
  now = datetime.datetime.now()
  today = datetime.date.today()
  tdy_date = today.strftime("%B %d, %Y")
  current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
  f = open(f"./log/{message.author.name}#{message.author.discriminator}.txt","a+")
  f.write(f"{message.author.name}#{message.author.discriminator} ({message.author.id}) wrote on {current_time}: {message.content}\n\n")
  f.close()
  await chn.send(embed=embed, components=[[Button(
      style=ButtonStyle.grey,
      label="Archive thread",
      custom_id="close"
  )]])

  for attachment in message.attachments:
    embed = discord.Embed(title="Incoming attachment", description="", color=discord.Colour.green())
    embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
    embed.set_image(url=attachment.proxy_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"User ID: {message.author.id}")
    f = open(f"./log/{message.author.name}#{message.author.discriminator}.txt","a+")
    f.write(f"{message.author.name}#{message.author.discriminator} ({message.author.id}) uploaded on {current_time}: {attachment.proxy_url}\n\n")
    f.close()
    await chn.send(embed=embed, components=[[Button(
      style=ButtonStyle.grey,
      label="Archive thread",
      custom_id="close"
  )]])
  await chn.send(embed=creationEmbed)


############ BUTTONS MODMAIL FUNCTION ############

async def shortcuts(interaction, msg):
  member = interaction.guild.get_member(int(interaction.channel.topic))
  embed = discord.Embed(title=f"Reply sent to {member.name}#{member.discriminator}", description=msg, color=discord.Colour.blue())
  embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator} ({config.getHighestRole(interaction.user)})", icon_url=interaction.user.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await interaction.channel.send(embed=embed, components=[[Button(
      style=ButtonStyle.grey,
      label="Close thread",
      custom_id="close"
  )]])

  embed = discord.Embed(title="", description=msg, color=discord.Colour.blue())
  embed.set_author(name=f"{interaction.user.name}#{interaction.user.discriminator} ({config.getHighestRole(interaction.user)})", icon_url=interaction.user.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await member.send(embed=embed)

  now = datetime.datetime.now()
  today = datetime.date.today()
  tdy_date = today.strftime("%B %d, %Y")
  current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
  f = open(f"./log/{member.name}#{member.discriminator}.txt","a+")
  f.write(f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}) wrote on {current_time}: {msg}\n\n")
  f.close()

############ SNIPPETS MODMAIL FUNCTION ############

async def snippets(ctx, msg):
  await ctx.message.delete()
  member = ctx.guild.get_member(int(ctx.message.channel.topic))
  embed = discord.Embed(title=f"Reply sent to {member.name}#{member.discriminator}", description=msg, color=discord.Colour.blue())
  embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} ({config.getHighestRole(ctx.author)})", icon_url=ctx.author.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=embed, components=[[Button(
      style=ButtonStyle.grey,
      label="Close thread",
      custom_id="close"
  )]])

  embed = discord.Embed(title="", description=msg, color=discord.Colour.blue())
  embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} ({config.getHighestRole(ctx.author)})", icon_url=ctx.author.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await member.send(embed=embed)

  now = datetime.datetime.now()
  today = datetime.date.today()
  tdy_date = today.strftime("%B %d, %Y")
  current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
  f = open(f"./log/{member.name}#{member.discriminator}.txt","a+")
  f.write(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) wrote on {current_time}: {msg}\n\n")
  f.close()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        

    if True:
      if isinstance(message.channel, discord.DMChannel):
        guild = bot.get_guild(config.GUILD_ID)
        category = bot.get_channel(config.CATEGORY_ID)
        for channel in category.channels:
          if str(channel.topic) == str(message.author.id):
            await message.add_reaction("✅")
            embed = discord.Embed(title="Incoming message", description=message.content, color=discord.Colour.green())
            embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"User ID: {message.author.id}")

            now = datetime.datetime.now()
            today = datetime.date.today()
            tdy_date = today.strftime("%B %d, %Y")
            current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
            f = open(f"./log/{message.author.name}#{message.author.discriminator}.txt","a+")
            f.write(f"{message.author.name}#{message.author.discriminator} ({message.author.id}) wrote on {current_time}: {message.content}\n\n")
            f.close()

            if message.content != "":
              await channel.send(embed=embed)

            attachments = message.attachments
            for attachment in attachments:
              embed = discord.Embed(title="Incoming attachment", description="", color=discord.Colour.green())
              embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=message.author.avatar_url)
              embed.set_image(url=attachment.proxy_url)
              embed.timestamp = datetime.datetime.utcnow()
              embed.set_footer(text=f"User ID: {message.author.id}")
              f = open(f"./log/{message.author.name}#{message.author.discriminator}.txt","a+")
              f.write(f"{message.author.name}#{message.author.discriminator} ({message.author.id}) uploaded on {current_time}: {attachment.proxy_url}\n\n")
              f.close()
              await channel.send(embed=embed)
            raise Exception()

        attachments = message.attachments
        if message.content != "":
          chn = await guild.create_text_channel(f"{message.author.name}#{message.author.discriminator}", category = category)
          await chn.edit(topic=message.author.id)
          await newThread(message, chn, guild)
      
        elif len(attachments) > 0:
          chn = await guild.create_text_channel(f"{message.author.name}#{message.author.discriminator}", category = category)
          await chn.edit(topic=message.author.id)
          await newThread(message, chn, guild)
    else:
      pass

    await bot.process_commands(message)


@bot.event
async def on_button_click(interaction):

############ MODMAIL MESSAGE BUTTONS ############

  if interaction.component.custom_id == "yes": 
    embed = discord.Embed(title="Closing Thread...", description="Thread will be closed in 5 seconds", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.channel.send(embed=embed)
    await interaction.message.delete()
    await asyncio.sleep(config.TIMEOUT)

    user = interaction.guild.get_member(int(interaction.channel.topic))
    log = bot.get_channel(config.LOG_CHANNEL)
    embed = discord.Embed(title="Thread closed", description=f"Thread created by {user.mention} is closed by {interaction.user.mention}", color=0xE44D41)
    embed.set_author(name=f"{user.name}#{user.discriminator}", icon_url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"User ID: {user.id}")
    await log.send(embed=embed)

    now = datetime.datetime.now()
    today = datetime.date.today()
    tdy_date = today.strftime("%B %d, %Y")
    current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
    f = open(f"./log/{user.name}#{user.discriminator}.txt","a+")
    f.write(f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id}) closed the thread on {current_time}.\n\n")
    f.close()
  
    await interaction.channel.delete()

  if interaction.component.custom_id == "no": 
    embed = discord.Embed(title="Action Cancelled", description=f"Alright {interaction.user.mention}! I will not close the thread!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    notice = await interaction.channel.send(embed=embed)
    await interaction.message.delete()
    await asyncio.sleep(config.TIMEOUT)
    await notice.delete()

  if interaction.component.custom_id == "close": 
    embed = discord.Embed(title="Are you sure about that?", description="This action is irreversible!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.channel.send(embed=embed, components=[[Button(
            style=ButtonStyle.green,
            label="Yes",
            custom_id="yes"
        ),Button(
            style=ButtonStyle.red,
            label="No",
            custom_id="no"
        )]])
    await interaction.respond()

  if interaction.component.custom_id == "memberYes": 
    embed = discord.Embed(title="Thread Closed!", description="Your thread has been closed! However, if needed, the community team may contact you again via this bot.", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.user.send(embed=embed)
    await interaction.message.delete()
    guild = bot.get_guild(config.GUILD_ID)
    category = bot.get_channel(config.CATEGORY_ID)
    for channel in category.channels:
      if str(channel.topic) == str(interaction.user.id):
        embed = discord.Embed(title="Thread closed by member!", description="The member decided that he/she no longer needs help. Use `!close` or click the respective button to close the thread.", color=discord.Colour.gold())
        embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed, components=[[Button(
            style=ButtonStyle.grey,
            label="Close thread",
            custom_id="close"
        )]])
        raise Exception()

  if interaction.component.custom_id == "memberNo": 
    embed = discord.Embed(title="Action Cancelled", description=f"Alright {interaction.user.mention}! I will not close the thread!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    notice = await interaction.user.send(embed=embed)
    await interaction.message.delete()
    await asyncio.sleep(config.TIMEOUT)
    await notice.delete()

  if interaction.component.custom_id == "memberClose": 
    embed = discord.Embed(title="Are you sure about that?", description="This action is irreversible!", color=0xFF0000)
    embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await interaction.user.send(embed=embed, components=[[Button(
            style=ButtonStyle.green,
            label="Yes",
            custom_id="memberYes"
        ),Button(
            style=ButtonStyle.red,
            label="No",
            custom_id="memberNo"
        )]])
    await interaction.respond()


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=config.STATUS))
    print(f'Logged in as {bot.user}')


############ MODMAIL SHORTCUT MESSAGES ############

@bot.command()
@has_permissions(administrator=True)
async def hi(ctx):
  await snippets(ctx, config.hi)

@bot.command()
@has_permissions(administrator=True)
async def transferred(ctx):
  await snippets(ctx, config.transferred)

@bot.command()
@has_permissions(administrator=True)
async def reported(ctx):
  await snippets(ctx, config.reported)

@bot.command()
@has_permissions(administrator=True)
async def morehelp(ctx):
  await snippets(ctx, config.morehelp)

@bot.command()
@has_permissions(administrator=True)
async def noreply(ctx):
  await snippets(ctx, config.noreply)

@bot.command()
@has_permissions(administrator=True)
async def canthelp(ctx):
  await snippets(ctx, config.morehelp)

############ MODMAIL REPLY COMMAND ############

@bot.command()
@has_permissions(administrator=True)
async def reply(ctx, *, msg):
    member = ctx.message.guild.get_member(int(ctx.message.channel.topic))
    await ctx.message.delete()
    embed = discord.Embed(title=f"Reply sent to {member.name}#{member.discriminator}", description=msg, color=discord.Colour.blue())
    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} ({config.getHighestRole(ctx.author)})", icon_url=ctx.author.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed, components=[[Button(
            style=ButtonStyle.grey,
            label="Close thread",
            custom_id="close"
        )]])

    embed = discord.Embed(title="", description=f"{msg}", color=discord.Colour.blue())
    embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator} ({config.getHighestRole(ctx.author)})", icon_url=ctx.author.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    await member.send(embed=embed)

    now = datetime.datetime.now()
    today = datetime.date.today()
    tdy_date = today.strftime("%B %d, %Y")
    current_time = f"{tdy_date} {now.strftime('%H:%M:%S')}"
    f = open(f"./log/{member.name}#{member.discriminator}.txt","a+")
    f.write(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) wrote on {current_time}: {msg}\n\n")
    f.close()

    attachments = ctx.message.attachments
    for attachment in attachments:
      embed = discord.Embed(title="", description="", color=discord.Colour.blue())
      embed.set_author(name=f"{ctx.author.name}", icon_url=ctx.author.avatar_url)
      embed.set_image(url=attachment.proxy_url)
      embed.timestamp = datetime.datetime.utcnow()
      await member.send(embed=embed)
      embed = discord.Embed(title=f"Attachment sent to {member.name}#{member.discriminator}", color=discord.Colour.blue())
      embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
      embed.set_image(url=attachment.proxy_url)
      embed.timestamp = datetime.datetime.utcnow()
      f = open(f"./log/{member.name}#{member.discriminator}.txt","a+")
      f.write(f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}) uploaded on {current_time}: {attachment.proxy_url}\n\n")
      f.close()
      await ctx.send(embed=embed)

@reply.error
async def reply_error(ctx, error):
  await ctx.send(f"```⚠️ {error}```")

############ MODMAIL CLOSE COMMAND ############

@bot.command()
@has_permissions(administrator=True)
async def close(ctx):
  embed = discord.Embed(title="Are you sure about that?", description="This action is irreversible!", color=0xFF0000)
  embed.set_author(name=f"{bot.user.name}#{bot.user.discriminator}", icon_url=bot.user.avatar_url)
  embed.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=embed, components=[[Button(
          style=ButtonStyle.green,
          label="Yes",
          custom_id="yes"
      ),Button(
          style=ButtonStyle.red,
          label="No",
          custom_id="no"
      )]])

keep_alive()

bot.run(config.TOKEN)