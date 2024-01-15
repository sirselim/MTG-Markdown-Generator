import requests

card_name = "Legolas, Master Archer"
base_url = "https://api.scryfall.com/cards/named"
params = {"exact": card_name}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    card_data = response.json()
    print(card_data)
else:
    print(f"Failed to fetch data for {card_name}. Status Code: {response.status_code}")