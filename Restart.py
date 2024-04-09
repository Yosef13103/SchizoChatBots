from Control import stop_bots, start_bots
import asyncio

# Stop the bots
stop_bots()

# Run the main function
asyncio.run(start_bots())
