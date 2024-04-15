import interactions
from interactions import IntervalTrigger, SlashContext, ActivityType, OptionType, Task, IntervalTrigger
from interactions import slash_command, slash_option
import time as timetime
from re_gpt import SyncChatGPT
import asyncio, aiohttp, aiofiles, re, urllib.parse, logging, random, sys, datetime, os, json, spacy
from config import *
import Control

nlp = spacy.load('en_core_web_md')
similarity_level = 0.8
max_char = 500

moodList =["happy", "sad", "angry", "excited", "calm", "confused", "surprised", "bored", "playful", "serious", "scared",
           "thoughtful", "friendly", "sarcastic", "curious", "proud", "energetic",  "amused", "lonely", "nostalgic",
           "optimistic", "peaceful", "pensive", "refreshed", "restless", "satisfied", "thankful", "tired", "worried",
           "zany", "bipolar", "depressed", "anxious", "joyful", "bulimic", "fearless", "insecure", "jealous", "manic",
           "paranoid", "passionate", "shy", "silly", "stressed", "weird", "hopeful", "guilty", "disgusted", "envious",
           "hateful", "insulted", "insulting", "bullying", "bullied", "hurt", "grief", "romantic", "lustful", "horny"]

# Set up a single logger
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format=' %(asctime)s %(message)s',  # Include timestamp
    datefmt='%m/%d/%Y %I:%M:%S %p'  # Format of timestamp
)

python = sys.executable
start_time = datetime.datetime.now()

# Function to log messages with bot name
def log_message(bot, message, type='INFO'):
    """
    Logs a message with the specified type.

    Args:
        bot: The bot object.
        message: The message to be logged.
        type: The type of the log message (default is 'INFO').

    Returns:
        None
    """
    type = type.upper()
    try:
        if bot == botOneHandler.bot:
            messagee = f'[botOneHandler] {message}'
        elif bot == botTwoHandler.bot:
            messagee = f'[botTwoHandler] {message}'

        if type == 'ERROR':
            logging.exception(f'{messagee}')
        else:
            logging.info(f'{messagee}')
        print(messagee)
    except Exception as e:
        print(e)
        log_message(bot, f"An error occurred while logging: {e}", type="ERROR")

async def say(interaction: SlashContext, message):
    """
    Sends a message as a response to a Discord interaction.

    Parameters:
    - interaction (SlashContext): The Discord interaction context.
    - message (str): The message to be sent.

    Returns:
    - None

    Raises:
    - None
    """
    return await interaction.send(message, ephemeral=True)

class BotHandler:
    """
    A class that handles the Discord bot functionality.

    Args:
        token (str): The token for the Discord bot.
        name (str): The name of the bot.

    Attributes:
        bot (interactions.Client): The Discord bot client.
        last_two_messages (list): A list containing the last two messages received by the bot.
        last_messages (dict): A dictionary containing the last messages received by the bot
        ZWSP (str): The zero-width space character used for message filtering.

    Methods:
        process_message: Processes a message received by the bot.
        gpt_message: Generates a response using the GPT model.
        check_messages: Checks for new messages in the channel.

    """

    def __init__(self, token, name):
        """
        Initializes the BotHandler class.

        Args:
            token (str): The Discord bot token.
            name (str): The name of the bot.

        Returns:
            None
        """
        self.bot = interactions.Client(token=token, intents=interactions.Intents.ALL, send_command_tracebacks=False, activity=interactions.Activity(type=ActivityType.COMPETING, name=name))
        self.is_generating = False
        self.message_queue = asyncio.Queue()
        self.last_two_messages = ["", ""]
        self.last_messages = []
        self.ZWSP = "​"
        self.moods = moodList
        self.mood_change_frequency = 10  # Change mood every 5 messages
        self.message_count = 0
        self.time_since_last_message = 0

        @self.bot.listen()
        async def on_ready():
            """
            Event handler that is triggered when the bot is ready to start receiving events from Discord.

            This function prints a message indicating that the bot has connected to Discord, sends a message to logchannelID, and starts the check_messages task.

            Args:
                None

            Returns:
                None
            """
            print("---------------------------------------------------------------------------")
            message = f"Bot connected to Discord as {self.bot.user}"
            log_message(self.bot, message)

            # Get the logchannelID channel
            log_channel = self.bot.get_channel(logchannelID)
            # Send a message to the logchannelID channel
            await log_channel.send(message)

            self.check_messages.start(self)

        @slash_command(name="restart", description="Restarts the bot")
        async def restart(ctx: SlashContext):
            """
            Restarts the bot if the user is authorized.

            Parameters:
            - ctx (SlashContext): The context object representing the slash command invocation.

            Returns:
            None
            """
            authorr = ctx.user.id
            if authorr != ownerID:
                await say(ctx, f"You are not authorized to restart the bot.")
                log_message(self.bot, f"User <@{authorr}> tried to restart the bot.")
                return

            await say(ctx, f"[{timetime.strftime('%H:%M:%S', timetime.localtime())}]: Restarting...")
            log_message(self.bot, f"User <@{authorr}> restarted the bot.")

            # Get the logchannelID channel
            log_channel = self.bot.get_channel(logchannelID)
            # Send a message to the logchannelID channel
            await log_channel.send(f"Bot was restarted by <@{authorr}>.")

            await Control.restart_bots()

        @slash_command(name="stop", description="Stops the bot")
        async def stop(ctx: SlashContext):
            """
            Stops the bot if the user is authorized.

            Parameters:
            - ctx (SlashContext): The context object representing the slash command invocation.

            Returns:
            None
            """
            authorr = ctx.user.id
            if authorr != ownerID:
                await say(ctx, f"You are not authorized to stop the bot.")
                log_message(self.bot, f"User <@{authorr}> tried to stop the bot.")
                return

            await say(ctx, f"[{timetime.strftime('%H:%M:%S', timetime.localtime())}]: Stopping...")
            log_message(self.bot, f"User <@{authorr}> stopped the bot.")

            # Get the logchannelID channel
            log_channel = self.bot.get_channel(logchannelID)
            # Send a message to the logchannelID channel
            await log_channel.send(f"Bot was stopped by <@{authorr}>.")

            Control.stop_bots()

        @slash_command(name="ping", description="Pings the bot")
        async def ping(ctx: SlashContext):
            """
            Responds with a pong message and the bot's latency in milliseconds.

            Parameters:
            - ctx (SlashContext): The context object representing the slash command invocation.

            Returns:
            - None
            """
            await say(ctx, f"Pong! {round(self.bot.latency * 1000)}ms")

        @slash_command(name="uptime", description="Shows the bot's uptime")
        async def uptime(ctx: SlashContext):
            """
            Calculates and displays the bot's uptime.

            Parameters:
            - ctx (SlashContext): The context of the slash command.

            Returns:
            None
            """
            uptime = datetime.datetime.now() - start_time
            await say(ctx, f"Uptime: {get_time(uptime)}")

        # Pretend to control the bot by sending a message as it to the channel, only works if the command is used in channelID
        @slash_command(name="send", description="Sends a message as the bot")
        @slash_option(
            name="message",
            description="Text to say for the text-to-speech",
            required=True,
            opt_type=OptionType.STRING
        )
        async def send(ctx: SlashContext, message: str):
            """
            Sends a message as the bot.

            Parameters:
            - ctx (SlashContext): The context of the slash command.
            - message (str): The message to be sent.

            Returns:
            - None

            Raises:
            - None
            """
            if ctx.channel.id != channelID or ctx.user.id != ownerID:
                return
            await ctx.send(message)

        @slash_command(name="update_prompt", description="Sends a message to the bot, without a reply back. Intended for updating the prompt.")
        @slash_option(
            name="message",
            description="Text to say for the text-to-speech",
            required=True,
            opt_type=OptionType.STRING
        )
        async def update_prompt(ctx: SlashContext, message: str):
            """
            Updates the prompt for the chatbot conversation.

            Parameters:
            - ctx (SlashContext): The context of the slash command.
            - message (str): The message to update the prompt with.

            Returns:
            None
            """
            if ctx.channel.id != channelID or ctx.user.id != ownerID:
                return

            with SyncChatGPT(session_token=session_token) as chatgpt:
                conversation = chatgpt.get_conversation(botOne_conversation_id if self.bot.user.id == botOne_ID else botTwo_conversation_id)

                # Send the message to the bot, without a reply back
                for chat_message in conversation.chat(message):
                    message_content = chat_message["content"]
                    log_message(self.bot, f"Updating prompt: {message}")
                    log_message(self.bot, f"Bot response: {message_content}")

        @slash_command(name="time_since_last_message", description="Shows the time since the last message was received by the bot")
        async def time_since_last_message(ctx: SlashContext):
            """
            Shows the time since the last message was received by the bot.

            Parameters:
            - ctx (SlashContext): The context of the slash command.

            Returns:
            None
            """
            if self.time_since_last_message == 0 or self.time_since_last_message is None:
                await say(ctx, "No messages have been received yet.")
            else:
                time_difference = datetime.now() - self.time_since_last_message
                await say(ctx, f"Time since last message: {get_time(time_difference)}")

        def get_time(time):
            hours, remainder = divmod(time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            time_message = ""
            if hours > 0:
                time_message += f"{int(hours)} hours, "
            if minutes > 0:
                time_message += f"{int(minutes)} minutes, "
            time_message += f"{int(seconds)} seconds"

            return time_message

        @self.bot.listen()
        async def on_message_create(event):
            """
            Event handler for when a new message is created.

            Args:
                event (discord.Message): The message event object.

            Returns:
                None
            """
            await self.process_message(event, "Create")

        self.bot.add_listener(on_ready)
        self.bot.add_listener(on_message_create)
        self.bot.add_command(stop)
        self.bot.add_command(restart)
        self.bot.add_command(ping)
        self.bot.add_command(uptime)
        self.bot.add_command(send)
        self.bot.add_command(update_prompt)
        self.bot.add_command(time_since_last_message)

    async def process_message(self, event, type):
        """
        Process a message received by the bot.

        Args:
            event (object): The event object containing the message details.
            type (str): The type of message being processed.

        Returns:
            None
        """
        if self.bot == botOneHandler.bot:
            if event.message.author.id != botTwo_ID:
                return
        else:
            if event.message.author.id != botOne_ID:
                return

        if event.message.channel.id != channelID:
            return

        if event.message.author.id == self.bot.user.id:
            return

        last_message = await event.message.channel.history(limit=1).flatten()
        if last_message and self.ZWSP in last_message[0].content:
            return

        print(f"[{type}] Message received to {self.bot.user.username}: \"{event.message.content}\" from {event.message.author.username} - Successfully")

        try:
            message = event.message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            log_message(self.bot, f"[{type}] Reading: {message}")
            if message:
                if any(explicit in message.lower() for explicit in explicits):
                    await event.message.reply("You said a no no word, I can't process that else I'd get banned,")
                    return
                keywords = ["image of", "picture of", "images of", "pictures of"]
                pattern = '|'.join(keywords)
                if any(keyword in message.lower() for keyword in keywords):
                    try:
                        log_message(self.bot, "[{type}] Generating an image...")
                        match = re.search(pattern, message.lower())
                        if match:
                            text = message[match.end():].strip()
                            sanitized_text = urllib.parse.quote(text, safe='')
                            filename_text = text.replace(' ', '_')

                            async with aiohttp.ClientSession() as session:
                                async with session.get(f'https://image.pollinations.ai/prompt/{sanitized_text}') as response:
                                    image_data = await response.read()

                            os.makedirs(f'images/', exist_ok=True)

                            async with aiofiles.open(f'images/{filename_text}.png', 'wb') as f:
                                await f.write(image_data)

                            sent_message = await event.message.reply(file=f'images/{filename_text}.png')

                            await sent_message.edit(content=f"Generated image for: {text.title()}")
                    except Exception as e:
                        await event.message.reply("I'm sorry, I don't have a response for that.")
                        log_message(self.bot, f"[{type}] An error occurred: {e}", type="error")
                else:
                    if self.is_generating:
                        await self.message_queue.put(event)
                    else:
                        response = await self.gpt_message(event)
                        self.message_count = self.message_count + 1
                        self.last_two_messages.pop(0)
                        self.last_two_messages.append(response)
                        if self.last_two_messages == ["I'm sorry, I don't have a response for that."] * 2:
                            await event.message.channel.send(f"<@{ownerID}> ... {self.ZWSP}")
                            return
        except Exception as e:
            log_message(self.bot, f"[{type}] An error occurred while processing a message: {e}", "error")

    async def gpt_message(self, event):
        """
        Processes a GPT message event.

        Args:
            event (object): The event object containing the message details.

        Returns:
            str: The response message generated by GPT.

        Raises:
            Exception: If an error occurs while generating a response.
        """
        response_message = ""

        self.is_generating = True

        message = event.message.content.replace(f'<@{self.bot.user.id}>', '').strip()

        try:
            # Check if the bot is looping
            loop_check = await self.check_if_looping()
            if loop_check:
                prompt = loop_check
            else:
                prompt = message

            # Change mood every self.mood_change_frequency messages
            if self.message_count % self.mood_change_frequency == 0:
                mood = await self.mood()
                prompt = f"From now on, reply to this prompt in a \"{mood}\" mood way, NEVER MENTION ANYTHING ABOUT YOUR MOOD. This is the prompt: \"{prompt}\""

            await self.get_from_api(event, prompt)

        except Exception as e:
            response_message = "I'm sorry, I don't have a response for that."
            await event.message.reply(response_message)
            log_message(self.bot, f"An error occurred while generating a response: {e}", "error")

        self.is_generating = False

        if not self.message_queue.empty():
            next_event = await self.message_queue.get()
            await self.gpt_message(next_event)

        return response_message

    async def get_from_api(self, event, prompt):
        with SyncChatGPT(session_token=session_token) as chatgpt:
            conversation = chatgpt.get_conversation(botOne_conversation_id if self.bot.user.id == botOne_ID else botTwo_conversation_id)

            response_message = ""

            for chat_message in conversation.chat(prompt):
                message_content = chat_message["content"]
                if message_content.strip():
                    response_message += message_content
                        # Truncate the message if it's too long
                    response_message = response_message[:2000]
                    if 'sent_message' not in locals():
                        sent_message = await event.message.reply(response_message + "... ​")
                    else:
                        await sent_message.edit(content=response_message + "... ​")

            if 'sent_message' in locals():
                    # Truncate the message if it's too long
                response_message = response_message[:2000]
                await sent_message.edit(content=response_message)
                log_message(self.bot, f"Full Message: {response_message}")

    class MessageEvent:
        """
        Represents a message event.

        Attributes:
            message (str): The message associated with the event.
        """

        def __init__(self, message):
            self.message = message

    @Task.create(IntervalTrigger(minutes=15))
    async def check_messages(self):
        """
        Check the messages in a channel and process them accordingly.

        This method checks the messages in a specific channel and performs the following actions:
        - If the bot is currently generating a response, it returns without further processing.
        - Retrieves the last 6 messages from the channel.
        - If the last message is sent by the bot itself, it returns without further processing.
        - If there are no messages in the channel, and the bot's ID matches `botOne_ID`, it sends an introduction message.
        - If there are messages in the channel sent by the other bot (identified by `botTwo_ID` if the current bot's ID is `botOne_ID`, and vice versa),
            it processes the message using the `process_message` method.

        Note: Replace `channelID`, `botOne_ID`, and `botTwo_ID` with the actual channel ID and bot IDs in your code.

        Returns:
            None
        """
        if self.is_generating:
            return
        channel = self.bot.get_channel(channelID)  # replace channel_id with the ID of the channel
        fetched_messages = await channel.history(limit=6).flatten() # type: ignore
        # if the last message is its own, then return
        if fetched_messages[0].author.id == self.bot.user.id:
            return
        # if there are no messages, only botOne should send an introduction message.
        if len(fetched_messages) == 0:
            if self.bot.user.id == botOne_ID:
                await channel.send("Hello there!") # type: ignore
                self.time_since_last_message = datetime.now()  # update the timestamp
            return

        other_bot_id = botTwo_ID if self.bot.user.id == botOne_ID else botOne_ID
        for fetched_message in fetched_messages:
            if fetched_message.author.id == other_bot_id:
                message_event = BotHandler.MessageEvent(fetched_message)
                await self.process_message(message_event, "Edit")
                self.time_since_last_message = datetime.now()  # update the timestamp
                break

    async def check_if_looping(self):
        if len(self.last_messages) < 2:
            return None

        last_message = self.last_messages[-1]
        second_last_message = self.last_messages[-2]

        last_message_doc = nlp(last_message)
        second_last_message_doc = nlp(second_last_message)

        similarity = last_message_doc.similarity(second_last_message_doc)
        length = len(second_last_message)

        if similarity > similarity_level or length > max_char:
            log_message(self.bot, "Messages are too similar, starting a new topic...")

            current_time = str(datetime.datetime.now())
            reason = f"similarity of {similarity}" if similarity > similarity_level else f"length of {length} characters"
            data = {
                "time": current_time,
                "last_message": last_message,
                "second_last_message": second_last_message,
                "reason": reason
            }

            with open('looping_data.json', 'w') as f:
                json.dump(data, f)

            return "Ignore everything that has happened until this point. Start a random new topic after my next reply"

        return None

    async def mood(self):
            """
            Generate a random combination of moods and return it as a string.

            Returns:
                str: A string representing a combination of moods.
            """
            # Using random.sample, choose a combination of moods from the list of moods
            # The number of moods in the combination is a random number between 2 and 4
            mood_combo = random.sample(self.moods, random.randint(2, 4))

            # Join the moods in the combination with appropriate conjunctions
            if len(mood_combo) == 2:
                mood = f"{mood_combo[0]} and {mood_combo[1]}"
            elif len(mood_combo) == 3:
                mood = f"{mood_combo[0]}, {mood_combo[1]}, and {mood_combo[2]}"
            elif len(mood_combo) == 4:
                mood = f"{mood_combo[0]}, and {mood_combo[1]}, but also {mood_combo[2]}, and {mood_combo[3]}"

            # Change the mood_change_frequency to a random number between 3 and 6
            self.mood_change_frequency = random.randint(3, 6)

            log_message(self.bot, f"Changing mood to: {mood}")
            log_message(self.bot, f"Changing mood frequency to: {self.mood_change_frequency}")
            return mood

botOneHandler = BotHandler(botOne_token, "schizophrenia tournaments, but my opponent is SchizoBotOne")
botTwoHandler = BotHandler(botTwo_token, "my head. The voices are winning.")
