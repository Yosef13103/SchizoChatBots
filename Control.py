import sys, asyncio, logging, time, subprocess, os
from BotHandler import botOneHandler, botTwoHandler

# Set up logging
class CustomFilter(logging.Filter):
    def filter(self, record):
        record.message = f'[🛠️ Bot Control] {record.getMessage()}'
        return True

logger = logging.getLogger()
logger.addFilter(CustomFilter())

logging.basicConfig(
    filename='bot.log',
    filemode="a",
    format='%(asctime)s - %(message)s',  # Include timestamp
    datefmt='%m/%d/%Y %I:%M:%S %p',  # Format of timestamp
    encoding='utf-8'  # Use utf-8 encoding
)

# Path to the Python interpreter that's running this script
python_path = sys.executable
run_py_path = "Run.py"  # replace with the actual path

# start_bot_one
async def start_bot_one():
    message = "Starting Bot One..."
    print(message)
    await botOneHandler.bot.astart(botOneHandler.bot.token)
    return message

# start_bot_two
async def start_bot_two():
    message = "Starting Bot Two..."
    print(message)
    await botTwoHandler.bot.astart(botTwoHandler.bot.token)
    return message

async def  start_bots():
    logging.info("-----------------------------------------------------------------------------------------------------------------------------")  # Log the message
    # Run both tasks in the same event loop
    results = await asyncio.gather(start_bot_one(), start_bot_two())
    start_bot_one_result, start_bot_two_result, _ = results
    logging.info(start_bot_one_result) # Log the message
    logging.info(start_bot_two_result) # Log the message

def stop_bots():
    logging.info("Stopping Bots...")

    # Read the PID from the text file
    with open('pid.txt', 'r') as f:
        pid = int(f.read())

    # Check the operating system
    if sys.platform == "win32":
        # Windows
        kill_command = f"taskkill /F /PID {pid}"
    else:
        # Unix-based system
        kill_command = f"kill {pid}"

    # Log the kill command
    logging.info(f"Running command: {kill_command}")

    # Kill the Run.py process
    subprocess.Popen(kill_command, shell=True)

    # Log that the process has been killed
    logging.info("Killed the bots.")

    # Delete the pid file
    os.remove("pid.txt")

def restart_bots():

    stop_bots()

    logging.info("Starting Bots...")
    # Command to start Run.py
    start_command = f"{python_path} {run_py_path}"

    # Log the start command
    logging.info(f"Running command: {start_command}")

    # Start Run.py again
    subprocess.Popen(start_command, shell=True)

    # Log that the process has been started
    logging.info("Started the bots.")
