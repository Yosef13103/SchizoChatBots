import os, sys, asyncio, logging, time
from BotHandler import botOneHandler, botTwoHandler

# Set up logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='[Bots] %(asctime)s %(message)s',  # Include timestamp
    datefmt='%m/%d/%Y %I:%M:%S %p'  # Format of timestamp
)

# Keep track of the tasks
bot_one_task = None
bot_two_task = None

# Starting
async def start_bot_one():
    try:
        message = "Starting Bot One..."
        print(message)
        await botOneHandler.bot.astart(botOneHandler.bot.token)
        while True:  # Keep the task running indefinitely
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await stop_bot_one()  # Stop the bot when the task is cancelled
        raise  # Re-raise the exception to propagate the cancellation

async def start_bot_two():
    try:
        message = "Starting Bot Two..."
        print(message)
        await botTwoHandler.bot.astart(botTwoHandler.bot.token)
        while True:  # Keep the task running indefinitely
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await stop_bot_two()  # Stop the bot when the task is cancelled
        raise  # Re-raise the exception to propagate the cancellation

async def start_bots():
    global bot_one_task, bot_two_task
    # delete quit.flag file if exists
    if os.path.exists("quit.flag"):
        os.remove("quit.flag")
    logging.info("-----------------------------------------------------------------------------------------------------------------------------")  # Log the message
    # Create tasks from the coroutines
    bot_one_task = asyncio.create_task(start_bot_one())
    bot_two_task = asyncio.create_task(start_bot_two())
    # Run all tasks in the same event loop
    results = await asyncio.gather(bot_one_task, bot_two_task, check_quit_flag(), return_exceptions=True)
    start_bot_one_result, start_bot_two_result, _ = results
    logging.info(start_bot_one_result) # Log the message
    logging.info(start_bot_two_result) # Log the message

# Stopping
async def stop_bot_one():
    if botOneHandler.bot.is_connected:
        message = "Stopping Bot One..."
        print(message)
    # Check if the bot is connected
        await botOneHandler.bot.stop()
    return message

async def stop_bot_two():
    if botTwoHandler.bot.is_connected:
        message = "Stopping Bot Two..."
        print(message)
        await botTwoHandler.bot.stop()
    return message

async def check_quit_flag():
    global bot_one_task, bot_two_task
    message = "Checking for quit flag"
    print(message)
    logging.info(message)  # Log the message

    if os.path.exists("quit.flag"):
        message = "Quit flag detected, Cancelling Tasks and Stopping Bots..."
        print(message)
        logging.info(message)  # Log the message
        if bot_one_task:
            bot_one_task.cancel()
            logging.info("Bot One Task Cancelled.")  # Log the cancellation
        if bot_two_task:
            bot_two_task.cancel()
            logging.info("Bot Two Task Cancelled.")  # Log the cancellation
        # Delete the "quit.flag" file
        os.remove("quit.flag")
        # Exit the script
        sys.exit()
    await asyncio.sleep(1)  # sleep for a while before checking again

def stop_bots():
    # Create the "quit.flag" file
    with open("quit.flag", "w") as file:
        pass

    time.sleep(4)

# Restarting
async def restart_bots():
    # Stop the bots
    stop_bots()

    # Start the bots
    await start_bots()

