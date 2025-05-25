# Binance Futures Trading Bot (Streamlit)

This is a simplified Binance Futures Trading Bot built with Python and Streamlit.  
It allows you to place market, limit, and stop-market orders on Binance Futures via the official Binance API.  
Additionally, it supports a **simulation mode** for safe testing without placing real orders.

---

## Features

- Place **MARKET**, **LIMIT**, and **STOP_MARKET** orders on Binance Futures
- Support for both **BUY** and **SELL** sides
- Fetch and display live market prices for user-specified trading pairs
- Simulation mode to **simulate order placement without sending real orders**
- Input validation for order parameters
- Logging of API requests, responses, and errors to `bot.log`
- Built with an interactive and user-friendly Streamlit web interface
- Auto-refresh live market price every 5 seconds

---

## Setup Instructions

### 1. Clone the repository (or copy the code)

```bash
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot
```

2. (Optional) Create and activate a Python virtual environment
bash
Copy
Edit
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```
4. Create a .env file in the project root with your Binance API keys

Create .env:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```
The bot supports SIMULATION_MODE = True so real keys are not required for basic testing.






5. Run the Streamlit app
```
streamlit run app.py

```
Your default browser will open the app UI.



ScreenShots:
![image](https://github.com/user-attachments/assets/3502fbd6-6082-4e47-bd08-5a8deb394f7b)
![image](https://github.com/user-attachments/assets/046fb69d-6150-4bd3-bf24-c0364f0865f2)
