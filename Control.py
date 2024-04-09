import os, sys, asyncio, logging, time
from BotHandler import botOneHandler, botTwoHandler

# Set up logging
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='[Bots] %(asctime)s %(message)s',  # Include timestamp
    datefmt='%m/%d/%Y %I:%M:%S %p'  # Format of timestamp
)

# start_bot_one
async def start_bot_one():
    message = "Starting Bot One..."
    print(message)
    await botOneHandler.bot.astart(botOneHandler.bot.token)
    return message

async def stop_bot_one():
    message = "Stopping Bot One..."
    print(message)
    await botOneHandler.bot.stop()
    return message

# start_bot_two
async def start_bot_two():
    message = "Starting Bot Two..."
    print(message)
    await botTwoHandler.bot.astart(botTwoHandler.bot.token)
    return message

async def stop_bot_two():
    message = "Stopping Bot Two..."
    print(message)
    await botTwoHandler.bot.stop()
    return message

async def check_quit_flag():
    message = "Checking for quit flag"
    print(message)
    logging.info(message)  # Log the message

    while True:
        if os.path.exists("quit.flag"):
            message = "Quit flag detected, stopping Bots"
            print(message)
            logging.info(message)  # Log the message
            try:
                stop_bot_one_result, stop_bot_two_result = await stop_bot_one(), stop_bot_two()
                logging.info(stop_bot_one_result) # Log the message
                logging.info(stop_bot_two_result) # Log the message
            except Exception as e:
                print(e)
                logging.error(e)
            finally:
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

async def start_bots():
    # delete quit.flag file if exists
    if os.path.exists("quit.flag"):
        os.remove("quit.flag")
    logging.info("-----------------------------------------------------------------------------------------------------------------------------")  # Log the message
    # Run both tasks in the same event loop
    results = await asyncio.gather(start_bot_one(), start_bot_two(), check_quit_flag())
    start_bot_one_result, start_bot_two_result, _ = results
    logging.info(start_bot_one_result) # Log the message
    logging.info(start_bot_two_result) # Log the message

async def restart_bots():
    # Stop the bots
    stop_bots()

    # Start the bots
    await start_bots()

