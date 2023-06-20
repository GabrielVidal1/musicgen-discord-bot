###############################################
#           Template made by Person0z         #
#          https://github.com/Person0z        #
#           Copyright© Person0z, 2022         #
#           Do Not Remove This Header         #
###############################################

# Imports
import disnake
import os

# Discord Token
token = os.getenv("TOKEN")

# Version
version = "1.0.0"

# Your Discord Server ID Will Go Here
guild = os.getenv("GUILD_ID")

# The Prefix You Want For Your Discord Bot
prefix = "!"

# Bot Status
activity = ["Jamming"]

# Colors
Success = disnake.Color.green
Error = disnake.Color.red
Random = disnake.Color.random

# Owner ID
owner_ids = [
    os.getenv("OWNER_ID")
]  # You can add more owner ids by adding a comma and the id

# Welcomes & Goodbyes Channel ID
welcome_channel = os.getenv("WELCOME_CHANNEL_ID")
join_role = "Newcomers"  # The role you want to give to new members

# Logging Channel ID
logs = [
    os.getenv("LOGS_CHANNEL_ID")
]  # You can add more channels by doing this: [channel_id, channel_id, channel_id]
