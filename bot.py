# Import libraries needed for the Discord bot
import discord           # Discord API library
import yfinance as yf   # For fetching stock data from Yahoo Finance
import asyncio         # For handling asynchronous tasks
import logging         # For logging bot activity and errors
from dotenv import load_dotenv  # To load environment variables from .env
import os              # To access environment variables
from discord.ext import tasks  # For scheduling repeated tasks

# Load environment variables from .env file
load_dotenv()

# Bot configuration using environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')  # Discord bot token
STOCK_TICKER = os.getenv('STOCK_TICKER')  # Stock ticker symbol (e.g., TSLA, AAPL, NVDA)

# Set up logging to console only (no file storage)
logging.basicConfig(
    level=logging.INFO,  # Log info, warnings, and errors
    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp
    handlers=[logging.StreamHandler()]  # Output to console only
)

# Set up Discord client with required intents
intents = discord.Intents.default()  # Use default intents
intents.message_content = False      # No need for message content
intents.guilds = True               # Enable server access for nickname updates
client = discord.Client(intents=intents)  # Create client (no commands)

# Event: Runs when bot connects to Discord
@client.event
async def on_ready():
    # Log that bot is ready
    logging.info(f'Bot is ready as {client.user}')
    try:
        # Start the update tasks if not running
        if not update_nickname.is_running():
            update_nickname.start()
        if not update_activity.is_running():
            update_activity.start()
    except Exception as e:
        # Log any errors starting the tasks
        logging.error(f'Error starting update tasks: {e}')

# Task: Update bot's nickname in all servers every 1.5 minutes
@tasks.loop(minutes=1.5)
async def update_nickname():
    try:
        # Fetch stock price from Yahoo Finance
        ticker = yf.Ticker(STOCK_TICKER)
        data = ticker.history(period='1d', interval='1m')  # Get 1-day data at 1-minute intervals
        if data.empty:
            logging.error(f'No {STOCK_TICKER} price data available')
            return
        price = data['Close'].iloc[-1]  # Get the most recent closing price

        # Update nickname in all servers with formatted price
        new_nickname = f"${price:,.2f}"
        for server in client.guilds:
            try:
                bot_member = server.get_member(client.user.id)
                if bot_member:
                    await bot_member.edit(nick=new_nickname)
                    logging.info(f'Nickname set to {new_nickname}')
                else:
                    logging.error('Bot member not found in a server')
            except discord.errors.HTTPException as e:
                # Log errors without server-specific data
                logging.error(f'Failed to update nickname: {e}')
            except Exception as e:
                # Log unexpected errors
                logging.error(f'Error updating nickname: {e}')

    except Exception as e:
        # Log any errors during nickname update
        logging.error(f'Error in update_nickname: {e}')

# Task: Update bot's activity every 5 minutes
@tasks.loop(minutes=5)
async def update_activity():
    try:
        # Fetch stock 24h change from Yahoo Finance
        ticker = yf.Ticker(STOCK_TICKER)
        data = ticker.history(period='1d', interval='1d')  # Get 1-day data
        if data.empty:
            logging.error(f'No {STOCK_TICKER} price data available for activity')
            return
        current_price = data['Close'].iloc[-1]  # Most recent price
        prev_close = ticker.info.get('previousClose', current_price)  # Previous day's close
        change_24h = ((current_price - prev_close) / prev_close) * 100  # Calculate % change

        # Clear current presence to avoid caching
        await client.change_presence(activity=None)
        await asyncio.sleep(0.5)  # Wait briefly to ensure clear
        # Set activity with 24h percentage change
        sign = '+' if change_24h >= 0 else ''  # Determine sign for percentage
        activity = discord.CustomActivity(name=f"{sign}{change_24h:.2f}% | {STOCK_TICKER} on NASDAQ.")
        await client.change_presence(activity=activity)
        # Log activity update
        logging.info(f'Activity set to: {sign}{change_24h:.2f}% | {STOCK_TICKER} on NASDAQ.')

    except Exception as e:
        # Log any errors during activity update
        logging.error(f'Error in update_activity: {e}')

# Ensure tasks wait for bot to be ready
@update_nickname.before_loop
@update_activity.before_loop
async def before_tasks():
    await client.wait_until_ready()  # Wait until bot is connected

# Run the bot
if __name__ == '__main__':
    try:
        client.run(BOT_TOKEN)  # Start bot with token
    except Exception as e:
        # Log any errors running the bot
        logging.error(f'Error running bot: {e}')
