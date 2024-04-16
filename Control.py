import os, sys, asyncio, logging, time
from BotHandler import botOneHandler, botTwoHandler

# Set up logging
logging.basicConfig(
    filename='bot.log',
    filemode="a",
    level=logging.INFO,
    format='%(asctime)s - [🛠️ Bot Control] %(message)s',  # Include timestamp
    datefmt='%m/%d/%Y %I:%M:%S %p'  # Format of timestamp
)

# start_bot_one
async def start_bot_one():
    message = "Starting Bot One..."
    print(message)
    await botOneHandler.bot.astart(botOneHandler.bot.token)
    return message

async def stop_bot_one():
    try:
        message = "Stopping Bot One..."
        print(message)
        await botOneHandler.bot.stop()
    except Exception as e:
        print(f"Error stopping bot one: {e}")
        logging.error(f"Error stopping bot one: {e}")
        message = None
    return message

# start_bot_two
async def start_bot_two():
    message = "Starting Bot Two..."
    print(message)
    await botTwoHandler.bot.astart(botTwoHandler.bot.token)
    return message

async def stop_bot_two():
    try:
        message = "Stopping Bot Two..."
        print(message)
        await botTwoHandler.bot.stop()
    except Exception as e:
        print(f"Error stopping bot two: {e}")
        logging.error(f"Error stopping bot two: {e}")
        message = None
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
                stop_bot_one_result = await stop_bot_one()
                logging.info(stop_bot_one_result) # Log the message
            except Exception as e:
                print(f"Error stopping bot one: {e}")
                logging.error(f"Error stopping bot one: {e}")

            try:
                stop_bot_two_result = await stop_bot_two()
                logging.info(stop_bot_two_result) # Log the message
            except Exception as e:
                print(f"Error stopping bot two: {e}")
                logging.error(f"Error stopping bot two: {e}")

            # Gather all running tasks
            tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

            # Wait for all tasks to complete
            if tasks:
                await asyncio.gather(*tasks)

            # Delete the "quit.flag" file
            os.remove("quit.flag")
            # Exit the script
            sys.exit()
        await asyncio.sleep(1)  # sleep for a while before checking again

async def stop_bots():
    try:
        # Create the "quit.flag" file
        with open("quit.flag", "w") as file:
            logging.info("quit.flag file created")
    except Exception as e:
        logging.error(f"Failed to create quit.flag file: {e}")

    time.sleep(5)

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
    await stop_bots()

    # Start the bots
    await start_bots()

