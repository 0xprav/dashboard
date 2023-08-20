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

def generatedata(filter_text):

    stake = sum(neuron.stake for neuron in neurons if filter_text in neuron.coldkey)
    emission = round(sum(neuron.emission for neuron in neurons if filter_text in neuron.coldkey) * 3, 3)
    hourlyemission = round(float(emission*taoprice),2)
    cashstake = round(float(stake*taoprice),2)
    return stake, emission, hourlyemission, cashstake


def drawpage():
    st.title(f"Miner Data")

    unique_coldkeys = set(neuron.coldkey for neuron in neurons)

    neuron_dict = {coldkey: [neuron for neuron in neurons if neuron.coldkey == coldkey] for coldkey in unique_coldkeys}
    total_emissions = {key: sum(neuron.emission for neuron in neuron_list)*3 for key, neuron_list in neuron_dict.items()}

# Sort the neuron_dict items by total emission in descending order
    sorted_items = sorted(neuron_dict.items(), key=lambda x: total_emissions[x[0]], reverse=True)

    for key, neuron_list in sorted_items:
        # Count of unique uids
        uid_count = len(set(neuron.uid for neuron in neuron_list))
        
        # Max, Min, and Average Emission
        emissions = [neuron.emission for neuron in neuron_list]
        max_emission = max(emissions)
        min_emission = min(emissions)
        avg_emission = sum(emissions) / len(emissions)
        
        # Total stake
        total_stake = sum(neuron.stake for neuron in neuron_list)
        
        st.write(f"Coldkey: {key}")
        st.write(f"hourly for Coldkey: {total_emissions[key]}")
        st.write(f"Total hourly earnings: {total_emissions[key] *taoprice}")
        st.write(f"Unique UIDs Count: {uid_count}")
        st.write(f"Max Emission: {max_emission}")
        st.write(f"Min Emission: {min_emission}")
        st.write(f"Average Emission: {avg_emission}")
        st.write(f"Total Stake: {total_stake}")
        st.write("-" * 50)  # A line separator for better readability


    # st.write("Hourly τ:", emission, "hourly $:", hourlyemission)
    # st.write("Total Stake:", stake, "total $ stake:",cashstake)
    # st.write("Current τ price:", taoprice)
    # st.markdown(f'*last updated:* {datetime.now().strftime("%I:%M %p %m/%d/%y ")}')



    # need data vis stuff

# Streamlit app
def main():
    refresh_data()
    # input_key = "filter_text_input"
    # filter_text = st.text_input("coldkey:", value="", key=input_key)
    # stake, emission, hourlyemission, cashstake= generatedata(filter_text)

    drawpage()

    # drawpage(filter_text,stake,emission,hourlyemission,cashstake)

    # if st.session_state[input_key] != filter_text:
    #     refresh_data()
    #     st.session_state[input_key] = filter_text
    #     st.write("Data automatically refreshed.")






if __name__ == "__main__":
    main()
