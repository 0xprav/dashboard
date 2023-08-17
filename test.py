import csv
import time
import requests
import bittensor as bt
from datetime import datetime



def get_price_data():
    response = requests.get("https://api.coingecko.com/api/v3/coins/bittensor/market_chart?vs_currency=USD&days=1&interval=daily")
    data = response.json()

    # Get the last index of the data
    last_data_point = {
        "prices": data["prices"][-1],
        "market_caps": data["market_caps"][-1],
        "total_volumes": data["total_volumes"][-1]
    }

    # Open a CSV file for writing
    with open('tao_price.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the last data point to the CSV
        csv_writer.writerow([
            last_data_point["prices"][0],
            last_data_point["prices"][1],
            last_data_point["total_volumes"][1]
        ])

def get_neuron_data(subnet: int):
    mt = bt.metagraph(netuid=subnet)
    neurons = mt.neurons


while True:  # This will create an infinite loop
    # Fetch the data from the API
    get_price_data()
    get_neuron_data(1)
    get_neuron_data(11)
    print(datetime.now())

    # Sleep for 20 minutes
    time.sleep(20 * 60)
