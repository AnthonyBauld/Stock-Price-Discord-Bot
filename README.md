# Stock Price Discord Bot

This Discord bot updates its nickname every 1.5 minutes to the current price of a chosen stock (e.g., "$245.67" for Tesla) and its activity every 5 minutes to the 24-hour percentage change (e.g., "+1.25% TSLA"). It uses the [yfinance](https://pypi.org/project/yfinance/) library to fetch real-time stock data from Yahoo Finance and can be configured to track any stock supported by Yahoo Finance.

![alt text](https://media.discordapp.net/attachments/1041966384428634162/1373847406512308295/Screenshot_2025-05-18_at_10.17.41_PM.png?ex=682be69a&is=682a951a&hm=01bc7f2a74bddf99704cc5cbea20ff89ab5995e2416732965b9d00002f0958a9&=&format=webp&quality=lossless&width=856&height=344 "Example")

## Features
- **Nickname Updates**: Displays the stock’s price as the bot’s nickname in all servers (requires "Change Nickname" permission).
- **Activity Updates**: Shows the 24-hour percentage change as the bot’s activity status.
- **Configurable Stock**: Easily change the stock by updating the `STOCK_TICKER` in `.env` (e.g., `TSLA`, `AAPL`, `NVDA`).
- **Console-Only Logging**: Logs updates and errors to the console without saving data to disk.
- **No Guild References**: Uses "server" instead of "guild" in logs and comments for clarity.

## Setup Instructions

### Prerequisites
- **Python 3.8+**: Ensure Python is installed (`python --version` or `python3 --version`).
- **Discord Bot Token**: Create a bot at [Discord Developer Portal](https://discord.com/developers/applications).
- **GitHub Repository**: Clone or download this repository to your local machine.

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/stock-price-discord-bot.git
   cd stock-price-discord-bot
   ```

2. **Create and Configure `.env`**
   - Create a `.env` file in the project root.
   - Add your Discord bot token and desired stock ticker:
     ```env
     BOT_TOKEN=your_discord_bot_token
     STOCK_TICKER=TSLA
     ```
   - Replace `your_discord_bot_token` with your bot’s token from the Discord Developer Portal.
   - Set `STOCK_TICKER` to your chosen stock (e.g., `AAPL` for Apple, `NVDA` for Nvidia). See [Changing the Stock](#changing-the-stock) for details.

3. **Install Dependencies**
   ```bash
   pip install discord.py yfinance python-dotenv
   ```
   - Ensure `pip` matches your Python version (try `pip3` or `python3 -m pip` if needed).

4. **Run the Bot**
   ```bash
   python stock_price_bot.py
   ```
   - Or use `python3 stock_price_bot.py` if required.
   - The bot will log in and start updating its nickname and activity.

5. **Invite the Bot to Servers**
   - In the Discord Developer Portal, go to **OAuth2 > URL Generator**.
   - Select `bot` scope and the **Change Nickname** permission.
   - Copy the generated URL and use it to invite the bot to your servers.
   - Ensure the bot has “Change Nickname” permission in each server.

6. **Verify Bot Behavior**
   - Check console logs for updates like:
     ```
     2025-05-18 21:45:12,123 - INFO - Bot is ready as StockBot#1234
     2025-05-18 21:46:42,456 - INFO - Nickname set to $245.67
     2025-05-18 21:50:12,457 - INFO - Activity set to: +1.25% TSLA
     ```
   - In Discord, confirm the bot’s nickname updates every 1.5 minutes (e.g., “$245.67”).
   - Check the bot’s activity updates every 5 minutes (e.g., “+1.25% TSLA”).

## Changing the Stock

To track a different stock, update the `STOCK_TICKER` in the `.env` file. The bot uses yfinance, which supports most stocks listed on Yahoo Finance (e.g., `TSLA`, `AAPL`, `NVDA`).

### Steps
1. **Find the Stock Ticker**
   - Visit [Yahoo Finance](https://finance.yahoo.com/) and search for your stock.
   - Note the ticker symbol (e.g., `AAPL` for Apple, `NVDA` for Nvidia, `MSFT` for Microsoft).
   - Test the ticker with yfinance:
     ```bash
     python -c "import yfinance as yf; print(yf.Ticker('AAPL').history(period='1d')['Close'].iloc[-1])"
     ```
     Ensure it returns a price (e.g., `175.23`). If it fails, the ticker may be invalid or delisted.

2. **Update `.env`**
   - Edit `.env` and change `STOCK_TICKER`:
     ```env
     BOT_TOKEN=your_discord_bot_token
     STOCK_TICKER=AAPL
     ```
   - Save the file.

3. **Restart the Bot**
   ```bash
   python stock_price_bot.py
   ```
   - The bot will now track the new stock (e.g., nickname: “$175.23”, activity: “+1.25% AAPL”).

### Supported Stocks
- **Common Tickers**: `TSLA` (Tesla), `AAPL` (Apple), `NVDA` (Nvidia), `MSFT` (Microsoft), `GOOGL` (Google), `AMZN` (Amazon).
- **Others**: Most stocks, ETFs, or indices listed on Yahoo Finance are supported. Search Yahoo Finance for the exact ticker.
- **Note**: Some tickers (e.g., international stocks) may require suffixes (e.g., `7203.T` for Toyota on Tokyo Exchange). Test with the yfinance command above.

## Troubleshooting
- **Bot Doesn’t Start**
  - Check `.env` for correct `BOT_TOKEN` and `STOCK_TICKER`.
  - Verify dependencies: `pip install discord.py yfinance python-dotenv`.
  - Ensure Python 3.8+: `python --version`.
  - Look for logs like “Error running bot: Invalid token”.

- **Nickname Doesn’t Update**
  - Check logs for “Bot member not found in a server” (bot not in server) or “Failed to update nickname” (e.g., missing permissions).
  - Ensure bot has “Change Nickname” permission in each server.
  - Verify bot is invited to servers.
  - Check for rate limit errors: “429 Too Many Requests”.

- **Activity Doesn’t Update**
  - Confirm logs show “Activity set to: +X.XX% <TICKER>” every 5 minutes.
  - Refresh Discord (Ctrl+R) or check on mobile.

- **yfinance Issues**
  - Test the ticker:
    ```bash
    python -c "import yfinance as yf; print(yf.Ticker('TSLA').history(period='1d')['Close'].iloc[-1])"
    ```
  - Ensure `STOCK_TICKER` is valid (e.g., `TSLA`, not `Tesla`).
  - Check for “No <TICKER> price data available” in logs, which may indicate a delisted stock or Yahoo Finance downtime.
  - yfinance may occasionally fail due to Yahoo Finance changes; retry or check [yfinance GitHub](https://github.com/ranaroussi/yfinance) for updates.

- **Logs**
  - All logs are console-only and use “server” (not “guild”).
  - Example errors: “Error in update_nickname: ...”, “Failed to update nickname: 403 Forbidden”.

## Contributing
- Fork the repository and submit pull requests for improvements.
- Suggest new features (e.g., multiple stock tracking, alternative data sources).

## License
MIT License. See [LICENSE](LICENSE) for details.
