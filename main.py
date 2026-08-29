import discord
import settings
from discord.ext import commands

import ia

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logou como {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Oi, sou {bot.user}!')

@bot.command()
async def reciclar(ctx):
    images = ctx.message.attachments

    for attachment in images:
        print("-x-x-x-x-x-x-x-x-x-x-x-x-x-")
        print(attachment.filename[:-4])
        print(attachment.url) 

        path = f"F:\\vscode\\Python\\Projetos\\Discord\\AI bot\\images\\{attachment.filename}"

        await attachment.save( #await nessa merda para parar de dar erro após 20 minutos
            path
            )

        lixo, dica = ia.reciclar(path)

        
        embed = discord.Embed(
            title=f"Isso aqui é um {lixo}",
            description=dica,
            color= 2067276
        )

        embed.set_image(url=attachment.url)

        embed.set_footer(text=lixo)

        await ctx.send(embed=embed)

bot.run(settings.info["chave"])