import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# member count 
def setup_member_counter(bot):
    CHANNEL_ID = 1499107568881238147

    async def update_member_count(guild):
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            await channel.edit(name=f"😼》atzen [ {guild.member_count} ]")

    @bot.event
    async def on_member_join(member):
        await update_member_count(member.guild)

    @bot.event
    async def on_member_remove(member):
        await update_member_count(member.guild)

    return update_member_count

update_member_count = setup_member_counter(bot)

@bot.event
async def on_ready():

    # bernd terminal start message
    print(f"{bot.user.name} is starting")

    # bermd restart message
    channel = bot.get_channel(1428566367350554764)
    if channel:
        await channel.send("Bin wieder da, mein Akh.")

    # member counter initial update
    for guild in bot.guilds:
        await update_member_count(guild)

# added custom emoji bei neuem user join
@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    
    if msg.type == discord.MessageType.new_member:
        emoji = discord.utils.get(msg.guild.emojis, name="pepeFlower")
        if emoji:
            await msg.add_reaction(emoji)
    
    await bot.process_commands(msg)
        

# !help - liste aller funktionen
@bot.command()
async def help(ctx):
    await ctx.send("```ansi\n"
        "\u001b[1;35mBernd's Funktionen\u001b[0m\n"
        "\u001b[37m────────────────────────────────\u001b[0m\n"
        "Bernd Basics:\n"
        "\u001b[33m!help        \u001b[0m– Zeigt diese Liste an\n"
        "\n"
        "Movement Ressourcen:\n"
        "\u001b[33m!bhop        \u001b[0m– Listet bugged FPS-Bereiche für Bhops auf\n"
        "\u001b[33m!climbspace  \u001b[0m– Sendet die 'Climb Space'-Grafik\n"
        "\u001b[33m!lurch       \u001b[0m– Verlinkt nützliche Lurch Ressourcen\n"
        "\u001b[33m!mantlejump  \u001b[0m– Verlinkt guten Mantlejump Guide\n"
        "\u001b[33m!superglide  \u001b[0m– Verlinkt nützliche Superglide Ressourcen\n"
        "\u001b[33m!ubounce     \u001b[0m– Verlinkt gutes 'Climb Zone' Video\n"
        "\u001b[33m!wiki        \u001b[0m– Verlinkt das Movement-Wiki\n"
        "\n"
        "Apex Zeugs:\n"
        "\u001b[33m!launch      \u001b[0m– Listet nützliche Launch Optionen\n"
        "\u001b[37m────────────────────────────────\u001b[0m\n"
        "```"
)

# !wiki - link zur apex movement wiki
@bot.command()
async def wiki(ctx):
    await ctx.send("Hier der Link zur Movement Wiki: \nhttps://apexmovement.tech/wiki")

# !superglide - link zum trainer und mokey video
@bot.command()
async def superglide(ctx):
    await ctx.send("Hier der Link zum Superglide Trainer & Guide: \nTrainer - https://apexmovement.tech/superglidetrainer/ \nGuide - https://www.youtube.com/watch?v=_cP1YO5Idts")

# !mantlejump - link zum theeb video
@bot.command()
async def mantlejump(ctx):
    await ctx.send("Hier der Link zum Mantlejump Guide: \nGuide - https://www.youtube.com/watch?v=69_lfGZz52Q")

# !lurch - link zum xzylas video
@bot.command()
async def lurch(ctx):
    await ctx.send("Hier der Link zum Lurch Guide: \nGuide - https://www.youtube.com/watch?v=JonGQ6F_p6E\n"
                   "Trainer by LiTTle - https://lurch-trainer.web.app/trainer")

# !ubounce - link zum eraiseddd video
@bot.command()
async def ubounce(ctx):
    await ctx.send("Hier der Link zu einem guten Guide: \nGuide - https://www.youtube.com/watch?v=RWEO8mERoCE")

# !bhop - angabe der bugged fps-bereiche
@bot.command()
async def bhop(ctx):
    await ctx.send("```ansi\n"
    "Diese \u001b[35mFPS-Bereiche\u001b[0m sind bugged:\n"
    "\u001b[37m───────────────────────────────\u001b[0m\n"
    "\u001b[35m 67 - 79 \u001b[0m\n"
    "\u001b[35m141 - 155 \u001b[0m\n"
    "\u001b[35m207 - 230 \u001b[0m\n"
    "\u001b[35m275 - 300 \u001b[0m\n"
    "\u001b[37m───────────────────────────────\u001b[0m\n"
    "```")

# !launch - liste von launch optionen
@bot.command()
async def launch(ctx):
    await ctx.send("```ansi\n"
    "Nützliche \u001b[35mLaunch Optionen\u001b[0m:\n"
    "\u001b[37m──────────────────────────\u001b[0m\n"
    "\u001b[35mcl_showpos  1 \u001b[0m       - Zeigt ingame nützliche Stats an (z.B. Velocity)\n"
    "\u001b[35mcl_showfps  4 \u001b[0m       - Zeigt die FPS an\n"
    "\u001b[35mcl_fovscale 1.7 \u001b[0m     - Stellt die FOV auf 120\n"
    "\u001b[37m──────────────────────────\u001b[0m\n"
    "```")

# !climbspace - sendet climbspace png
@bot.command()
async def climbspace(ctx):
    file_path = os.path.join(
        os.path.dirname(__file__),
        "graphics",
        "graphic_climb_space_with_zones_light.png"
    )
    await ctx.send(file=discord.File(file_path))

#------------------------------ADMIN---------------------------------#
# !clear - cleart n + 1 der letzten nachrichten
@bot.command()
@commands.has_role("Guides")
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)