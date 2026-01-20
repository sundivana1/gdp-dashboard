import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='My trade',
    page_icon=':share market:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import pyotp
import pandas as pd

# 1. Setup Connection
api_key = "YOUR_API_KEY"
client_id = "YOUR_CLIENT_ID"
pwd = "YOUR_PASSWORD"
totp_key = "YOUR_TOTP_KEY"

obj = SmartConnect(api_key=api_key)
data = obj.generateSession(client_id, pwd, pyotp.TOTP(totp_key).now())
feed_token = obj.getfeedToken()

# 2. Strategy Logic: Breakout Detection
def check_breakout(df):
    # Resistance = Highest price of the last 15 candles
    resistance = df['high'].iloc[-16:-1].max() 
    current_price = df['close'].iloc[-1]
    
    if current_price > resistance:
        print(f"🚀 BREAKOUT DETECTED at {current_price}!")
        # Add your code here to send a mobile notification or sound an alarm

# 3. Live WebSocket Handling
def on_data(wsapp, message):
    # This function runs every time a new price comes from Nifty
    ltp = message['last_traded_price'] / 100
    print(f"Nifty Live Price: {ltp}")
    # In a full app, you'd collect these prices into a dataframe and call check_breakout()

sws = SmartWebSocketV2(data["data"]["jwtToken"], api_key, client_id, feed_token)
sws.on_data = on_data
sws.connect()
