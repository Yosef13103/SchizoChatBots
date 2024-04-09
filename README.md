# SchizoChatBots

This project contains two Discord bots, BotOne and BotTwo, that simulate (hopefully) endless conversations.
The project is used to handle communication from the ChatGPT Website to Discord. Any actual responses are completely based on the prompt used and the model used.

## Project Structure

### Setup

1. Install the required packages by running `setup.py`. This will install the required packages and create the `config.py` file.
2. Fill in the necessary values in the `config.py` file. This includes the Discord ID of the bot owner, a list of explicit words or phrases that the bot should not read, the ID of the Discord channel where the bot operates, and tokens for session authentication and the bots.
3. Please read more about [re_gpt](https://github.com/Zai-Kun/reverse-engineered-chatgpt) libary for more information on how to setup the ChatGPT bots.
4. Setup the bots themselves on the [ChatGPT](https://chat.openai.com/) website. Using whatever prompts you want for the two bots.

### Usage

- To start the bots, run `Run.py`.
- To stop them, run `Stop.py`.
- To restart them, run `Restart.py`.

## BotHandler

The `BotHandler.py` file contains the `BotHandler` class, which handles the Discord bot functionality. It processes messages received by the bot, generates responses using the GPT model, and checks for new messages in the channel.

The `BotHandler` class utilizes the [re_gpt](https://github.com/Zai-Kun/reverse-engineered-chatgpt) library, a reverse-engineered version of OpenAI's GPT-3 model, for generating responses to the processed messages.

The `re_gpt` library provides a Python interface for interacting with the GPT-3 model. It allows the bot to generate human-like responses to incoming messages.

When a new message is received, the `BotHandler` class processes it and passes the content to the `re_gpt` library. The library uses the GPT-3 model to generate a response, which is then sent back to the Discord channel.

This integration with the `re_gpt` library allows the bot to engage in dynamic and human-like conversations on the Discord channel.

### Message Processing

The `BotHandler` class processes incoming messages from the Discord channel. It ensures that the message is from the correct channel and not from the same bot. It also checks if the message is from the other bot.

### Response Generation

The `BotHandler` class generates responses to the processed messages using a GPT model. The responses are designed to be as human-like as possible.

### Message Checking

The `BotHandler` class checks for new messages in the Discord channel. It ensures that the bot responds to new messages in a timely manner.

## Logging

The bots' activities are logged in `bot.log`. This includes the messages received and sent by the bots, as well as any errors or exceptions that occur.

## Image Generation

The bots can generate images using the [Pollinations AI](https://image.pollinations.ai/) service. This service uses AI models to generate images based on text prompts.

To request an image, a message must contain one of the following keywords: "image of", "picture of", "images of", "pictures of". The text following any of these keywords is used as the prompt for the image generation.

For example, if a message contains "image of a sunset", the bot will send a request to the Pollinations AI service with "a sunset" as the prompt. The service will then generate an image based on this prompt and return it to the bot.

The generated image is saved in the `images/` directory and are sent into the discord channel.

Please note that the quality and relevance of the generated images depend on the clarity and specificity of the prompt. The filter is not in my hands, and anything can be generated.

## Commands

### Python Scripts

The `Control.py` file contains functions to start, stop, and restart the bots.

The bots can be controlled using the following commands:

- `Run.py`: Starts the bots.
- `Stop.py`: Stops the bots.
- `Restart.py`: Restarts the bots.

## Discord Commands

The bot supports several commands that can be invoked using Discord's slash command feature. These commands were created using the [interactions.py](https://github.com/interactions-py/interactions.py) library. Here are the details of these commands:

### /restart

The `/restart` command restarts the bot. This command can only be used by the bot owner. If an unauthorized user tries to use this command, the bot will respond with a message indicating that the user is not authorized to restart the bot.

### /ping

The `/ping` command checks the bot's latency. The bot responds with a message containing the word "Pong!" and the bot's latency in milliseconds.

### /uptime

The `/uptime` command displays the bot's uptime. The bot responds with a message containing the bot's uptime in hours, minutes, and seconds.

### /send

The `/send` command sends a message as the bot. This command can only be used in a specific channel and by the bot owner. The message to be sent is provided as an argument to the command.

## Acknowledgement
- [interactions.py](https://github.com/interactions-py/interactions.py) | Discord API
- [re_gpt](https://github.com/Zai-Kun/reverse-engineered-chatgpt) | ChatGPT API
- [Pollinations AI](https://image.pollinations.ai/) | Image Generation