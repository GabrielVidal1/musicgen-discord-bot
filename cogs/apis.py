###############################################
#           Template made by Person0z         #
#          https://github.com/Person0z        #
#           Copyright© Person0z, 2022         #
#           Do Not Remove This Header         #
###############################################

# Importing Libraries
import disnake
from disnake.ext import commands
import os
import aiohttp
import base64
import time
from PIL import Image
from io import BytesIO
import random
import json
import config
from helpers import errors
from .musicgen.banana_client import generate_musicgen

class Apis(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Loaded Cog API')

    # Image Genertor
    @commands.slash_command(name="generate", description="Generate an image from a prompt!")
    async def generate(inter, *, prompt: str):
        try:
            await inter.response.defer()
            ETA = int(time.time() + 60)
            loading_images = ["assets/loading/loading.gif",
                            "assets/loading/loading2.gif",
                            "assets/loading/loading3.gif", 
                            "assets/loading/loading4.gif",
                            "assets/loading/loading5.gif"]
            embed = disnake.Embed(title=f"Loading...! Generating image... ETA: <t:{ETA}:R>", color=disnake.Color.random())
            embed.set_image(file=disnake.File(random.choice(loading_images)))
            await inter.send(embed=embed)
            async with aiohttp.request("POST", "https://backend.craiyon.com/generate", json={"prompt": prompt}) as resp:
                if resp.status != 200:
                    return await inter.edit_original_response(content="An error occurred while generating the image.")
                data = await resp.json()
                img = Image.open(BytesIO(base64.b64decode(data["images"][0])))
                img.save("image.png")
                embed = disnake.Embed(title=f"The image you wanted generated: {prompt}", color=disnake.Color.random())
                embed.set_image(file=disnake.File('image.png'))
                await inter.edit_original_response(content=None, embed=embed)
                os.remove("image.png")
        except Exception as e:
            embed = disnake.Embed(title=f"Error", color=disnake.Color.red())
            embed.add_field(name="Error", value=f"An error occurred while generating the image.\n{str(e)}")
            await inter.edit_original_response(embed=embed)

    @commands.slash_command(name="musicgen", description="Generate a music")
    async def generate_musicgen(
        inter: disnake.ApplicationCommandInteraction,
        prompt: str = commands.Param(description="The prompt to generate the music from"),
        duration: int = commands.Param(description="The duration of the music to generate", default=8, choices=[4, 8, 10, 12, 14, 16, 18, 20]),
    ):
        
        try:
            await inter.response.defer()

            ETA = int(time.time() + 15 * duration)
            embed = disnake.Embed(title=f"Loading...! Generating music... ETA: <t:{ETA}:R>", color=disnake.Color.random())
            embed.set_image(file=disnake.File("assets/loading/loading_music.gif"))
            await inter.send(embed=embed)

            path, filename = generate_musicgen(prompt, duration)
            file = disnake.File(path, filename=filename)

            content = f"{inter.author.mention} **{prompt}**"
            await inter.edit_original_response(file=file, content=content, embed=None)

        except Exception as e:
            embed = disnake.Embed(title=f"Error", color=disnake.Color.red())
            embed.add_field(name="Error", value=f"An error occurred while generating the music.\n{str(e)}")
            await inter.edit_original_response(embed=embed, file=None, content=None)




    # # Animal Slash Command with options for different animals 
    # @commands.slash_command()
    # async def animal(
    #     inter: disnake.ApplicationCommandInteraction,
    #     action: str = commands.Param(choices=["bird", "dog", "cat", "fox", "koala", "panda"]),
    # ):
    
    #     colors = {
    #         "bird": disnake.Color.blue(),
    #         "dog": disnake.Color.green(),
    #         "cat": disnake.Color.orange(),
    #         "fox": disnake.Color.purple(),
    #         "koala": disnake.Color.dark_green(),
    #         "panda": disnake.Color.dark_gold(),
    #     }
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             request = await session.get(f'https://some-random-api.ml/img/{action}')
    #             animaljson = await request.json()
    #             request2 = await session.get(f'https://some-random-api.ml/facts/{action}')
    #             factjson = await request2.json()
    #             embed = disnake.Embed(title=f"{action.title()} Image", color=colors[action])
    #             embed.set_image(url=animaljson['link'])
    #             embed.add_field(name=f"{action.title()} Fact", value=factjson['fact'])
    #             embed.set_footer(text=f'Requested by {inter.author} ', icon_url=inter.author.avatar.url)
    #             await inter.send(embed=embed)
    #     except Exception as e:
    #         await inter.send(embed=errors.create_error_embed(f"Error sending animal command: {e}"))
            
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if message.author.bot:
    #         return
    #     if len(message.attachments) > 0:
    #         if message.attachments[0].url.endswith(('.txt', '.js', '.py', '.c', '.cpp', '.java', '.html', '.css', '.scss')) == True:
    #             download = message.attachments[0].url
    #             async with aiohttp.ClientSession() as session:
    #                 async with session.get(download, allow_redirects=True) as r:
    #                     text = await r.text()
    #                     text = "\n".join(text.splitlines())
    #                     truncated = False
    #                     if len(text) > 100000:
    #                         text = text[:99999]
    #                         truncated = True
    #                     req = requests.post('https://paste.zluqe.com/documents', data=text)
    #                     key = json.loads(req.content)['key']
    #                     response = ""
    #                     response = response + "https://paste.zluqe.com/" + key
    #                     response = response + "\nRequested by " + message.author.mention
    #                     if truncated:
    #                         response = response + "\n(file was truncated because it was too long.)"
    #                     embed = disnake.Embed(title="Please Use The Zluqe Paste Service", color=0x1D83D4)
    #                     embed.add_field(name='Paste URL', value=f'> [File Paste Link](https://paste.zluqe.com/{key})')
    #                     embed.add_field(name='File Extension', value='> '+ download.split('.')[-1])
    #                     embed.add_field(name='File Size', value='> '+ str(round(len(text)/1000)) + ' KB')
    #                     embed.set_footer(text=f'Requested by {message.author}', icon_url=message.author.avatar.url)
    #                     await message.reply(embed=embed)
    #         else:
    #             return

def setup(bot):
    bot.add_cog(Apis(bot))
