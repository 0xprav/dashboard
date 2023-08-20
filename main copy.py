import asyncio
import requests
import streamlit as st
from datetime import datetime

asyncio.set_event_loop(asyncio.new_event_loop())

neurons = []

def initialize_bittensor():
    global bt
    import bittensor as bt


# Convert this function to asynchronous
async def refresh_data_async():
    global neurons
    global taoprice
    response = requests.get("https://api.coingecko.com/api/v3/coins/bittensor/market_chart?vs_currency=USD&days=1&interval=daily")
    taoprice = round(response.json()['prices'][-1][-1],2)
    initialize_bittensor()
    mt = bt.metagraph(netuid=1)  # Assuming this is an async call
    neurons = mt.neurons

# Synchronous wrapper for the async function
def refresh_data():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(refresh_data_async())

# Streamlit app
def main():
    refresh_data()
    # Create a toggle button widget
    # Display the selected value

    # Create a unique key for the text input to track changes
    input_key = "filter_text_input"

    # Automatically refresh data when the input changes
    filter_text = st.text_input("coldkey:", value="", key=input_key)

    st.title(f"Miners up : {sum(1 for neuron in neurons if filter_text in neuron.coldkey)}")

    # Initial data load
    stake = sum(neuron.stake for neuron in neurons if filter_text in neuron.coldkey)
    emission = round(sum(neuron.emission for neuron in neurons if filter_text in neuron.coldkey) * 3, 3)
    hourlyemission = round(float(emission*taoprice),2)
    cashstake = round(float(stake*taoprice),2)
    st.write("Hourly τ:", emission, "hourly $:", hourlyemission)
    st.write("Total Stake:", stake, "total $ stake:",cashstake)
    st.write("Current τ price:", taoprice)
    st.markdown(f'*last updated:* {datetime.now().strftime("%I:%M %p %m/%d/%y ")}')

    # Automatically refresh data using the text input's unique key
    if st.session_state[input_key] != filter_text:
        refresh_data()
        st.session_state[input_key] = filter_text
        st.write("Data automatically refreshed.")

if __name__ == "__main__":
    main()
