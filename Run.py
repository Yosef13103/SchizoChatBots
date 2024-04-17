import asyncio
from Control import start_bots
import os

pid = os.getpid()

# Write the PID to a text file
with open('pid.txt', 'w') as f:
    f.write(str(pid))

# Start the bots
asyncio.run(start_bots())