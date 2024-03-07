import os
import traceback
import urllib.request

import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFilter

# Importing bot utils
from core.ConfigManager import ConfigManager
# Object that contains all the config data from the config.json file
config = ConfigManager()


def generate_image(user_name, user_icon_url):
    try:
        bg_image = Image.open("./assets/greetings/background.jpg").resize((1920, 700))

        bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))

        bg_overlay = Image.new("RGBA", bg_image.size, (0, 0, 0, 128))

        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent",
                              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(str(user_icon_url), f"./assets/greetings/UserProfilePictures/user_image_{user_name.lower()}.png")

        user_image = Image.open(f"./assets/greetings/UserProfilePictures/user_image_{user_name.lower()}.png").resize((550, 550))

        user_icon = Image.new("RGBA", bg_image.size, (0, 0, 0, 0))

        mask = Image.new("L", user_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + user_image.size, fill=255)

        user_icon.paste(user_image, (120, 80), mask=mask)

        logo = Image.open("./assets/greetings/logo.png").resize((950, 665))

        user_icon.paste(logo, (870, 65))

        bg_image.paste(bg_overlay, (0, 0), mask=bg_overlay)
        bg_image.paste(user_icon, (0, 0), mask=user_icon)

        os.remove(f"./assets/greetings/UserProfilePictures/user_image_{user_name.lower()}.png")
        bg_image.save(f"./assets/greetings/WelcomeImages/welcome_image_{user_name.lower()}.png")
        return f"./assets/greetings/WelcomeImages/welcome_image_{user_name.lower()}.png"
    except Exception as e:
        print(f"Error: {print(e)}")
        traceback.print_exc()


class Greetings(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{config.bot_prefix} The 'Greetings' extension is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        try:
            welcome_image = generate_image(str(member)[:-5], member.display_avatar)
            if channel is not None:
                await channel.send(file=discord.File(welcome_image))
                await channel.send(f"*{member.mention}* **{config.greetings_ext_welcome_message}**")
                os.remove(welcome_image)
        except Exception as e:
            print(f"{config.bot_prefix} An error {e} has occurred while trying to generate the welcome image")

            traceback.print_exc()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Grabbing the id of the system channel
        channel = member.guild.system_channel
        # Check if there is a goodbye message in the config.json
        if config.greetings_ext_goodbye_message:
            # If there is a message for goodbye, it will send a goodbye message to the system channel
            await channel.send(f"*{member.mention}* **{config.greetings_ext_goodbye_message}**")


# Exporting the class
async def setup(bot):
    await bot.add_cog(Greetings(bot))
