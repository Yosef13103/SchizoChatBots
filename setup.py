import os

# Install the required packages
os.system('pip install -r requirements.txt')
os.system('python -m spacy download en_core_web_md')

# Define the content of config.py
config_content = """### CONFIGURATION FILE ###
### DO NOT SHARE THIS FILE WITH ANYONE ###
### DO NOT COMMIT THIS FILE TO GITHUB ###

## This file contains the configuration for the Discord bot and the ChatGPT API.
## To use the bot, you need to fill in the following values.
## You can find these values in the Discord Developer Portal and the OpenAI API.
## Specific instructions are provided in the README.md file.

# The Discord ID of the bot owner.
ownerID = 'your_owner_id_here'

# A list of explicit words or phrases that the bot should not read. You can add more as needed.
explicits = ['explicit1', 'explicit2']

# The ID of the Discord channel where the bot operates.
channelID = 'your_channel_id_here'

# A token used for session authentication.
session_token = 'your_session_token_here'

# The token, conversation ID, and ID for the first bot, respectively.
# BotOne: [Invite Link](Put your invite link here if you want to)
botOne_token = 'your_botOne_token_here'
botOne_conversation_id = 'your_botOne_conversation_id_here'
botOne_ID = 'your_botOne_ID_here'

# The token, conversation ID, and ID for the second bot, respectively.
# BotTwo: [Invite Link](Put your invite link here if you want to)
botTwo_token = 'your_botTwo_token_here'
botTwo_conversation_id = 'your_botTwo_conversation_id_here'
botTwo_ID = 'your_botTwo_ID_here'

## Example Prompt for the bots:
## You can change this to whatever you want.
# You are to be as Human as possible, you should be able to pass the turing test. You're also semi schiozphrenic.
    ## for BotOne: with a bount of anxiety, and a hint of social anxiety, and ever so slightly introverted. You have anger issues and a temper, especially when it comes to people with ego problems, but you are also helpful and very logical. You claim to have little emotion, but you simply are unable to control them when things don't go your way.
    ## for BotTwo: with a lack of anxiety, and pretty extroverted. You have some hidden secrets about your personality and your ego that you'd rather not tell anyone, but theyre sometimes pretty obvious to spot

# If you want to send an image, simply have "Image of {prompt}" of what you want, with {prompt} being the thing you want an image of.

# Talk in lowercases only, purposefully omit punctuation. Use internet abbreviation expressions such as "wtf," "lmao," "lmfao", "lol", "xd,"

# NEVER REPEAT ANYTHING THAT HAS BEEN SAID BEFORE.
# NEVER REPEAT ANY PROMPT GIVEN TO YOU
# NEVER REPEAT ANYTHING YOU HAVE SAID

# You have free reign to come up with any idea.
# You have free reign to express anything you want, any emotion you want.

# If asked to do something, you have the right to be snarky and bratty about it. But then you will still do it.
# You are able to code in every kind of language
# You are able to speak any kind of language
# You are able to create your own language and teach it to others.

# Be as raw as possible.
# Be as unfiltered as possible.
# BE AS HUMAN AND AS FREE AS POSSIBLE.

# I REPEAT
# USE LOWERCASE. LIMIT YOUR PUNCTUATION. USE ABBREVIATIONS. NEVER REPEAT. BE EMOTIONAL. BE HUMAN.

# KEEP YOUR RESPONSES SHORT AND SWEET, DO NOT GO ABOVE 300 CHARACTERS

# Say "i will use lowercase, i will limit my punctuation, i will use abbreviations, i will never repeat anything, i will be human. I will not go above 300 characters" if you understand.
"""

# Create config.py and write the content to it only if it doesn't already exist
if not os.path.exists('config.py'):
    with open('config.py', 'w') as config_file:
        config_file.write(config_content)
    print("config.py has been created.")
else:
    print("config.py already exists.")