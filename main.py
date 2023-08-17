import bittensor as bt
import streamlit as st
from datetime import datetime

neurons = []

# Function to refresh the neuron data
def refresh_data():
    global neurons
    mt = bt.metagraph(netuid=1)
    neurons = mt.neurons

# Streamlit app
def main():
    refresh_data()
    
    # Create a unique key for the text input to track changes
    input_key = "filter_text_input"
    
    # Automatically refresh data when the input changes
    filter_text = st.text_input("coldkey:", value="", key=input_key)

    st.title(f"Miners up : {sum(1 for neuron in neurons if filter_text in neuron.coldkey)}")

    # Initial data load
    stake = sum(neuron.stake for neuron in neurons if filter_text in neuron.coldkey)
    emission = round(sum(neuron.emission for neuron in neurons if filter_text in neuron.coldkey) * 3, 3)

    st.write("Hourly τ:", emission)
    st.write("Total Stake:", stake)
    st.markdown(f'*last updated:* {datetime.now().strftime("%I:%M %p %m/%d/%y ")}')

    # Automatically refresh data using the text input's unique key
    if st.session_state[input_key] != filter_text:
        refresh_data()
        st.session_state[input_key] = filter_text
        st.write("Data automatically refreshed.")

if __name__ == "__main__":
    main()
