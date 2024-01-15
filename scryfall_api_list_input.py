#!/Users/Miles.Benton/homebrew/bin/python3 
import os
import sys
import requests
import concurrent.futures
import re
from urllib.parse import urlencode
from tqdm import tqdm
import time

# Add a global variable to track verbosity
verbose_output = False

def find_card_by_name(card_name):
    base_url = "https://api.scryfall.com/cards/named"
    params = {"exact": card_name}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data  # Return the direct result

    print(f"Failed to find card '{card_name}'. Status Code: {response.status_code}")
    
    # Print the API response for debugging
    print(response.text)
    
    return None

def download_image(image_url, filename):
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)

        if verbose_output:
            print(f"Image downloaded successfully as {filename}")
        return True
    else:
        print(f"Failed to download image from {image_url}")
        return False

def get_scryfall_url(card_name):
    # Construct the Scryfall card URL with quotes around the search term
    return f"https://scryfall.com/search?q=\"{card_name.replace(' ', '+')}\""

def generate_markdown_table(card_list):
    # Sort the card list alphabetically by card name
    card_list.sort(key=lambda x: x[0])

    markdown_table = "|   |   |   |\n"
    markdown_table += "|---|---|---|\n"

    for i in range(0, len(card_list), 3):
        row = card_list[i:i + 3]

        markdown_table += "|"

        for card_name, set_code, collector_number, card_data in row:
            scryfall_url = get_scryfall_url(card_name)
            alt_text = card_name.replace('_', ' ')

            if card_data:
                # Check if the card is double-faced
                card_faces = card_data.get("card_faces")
                if card_faces:
                    image_uris = card_faces[0].get("image_uris", {})
                else:
                    image_uris = card_data.get("image_uris", {})

                image_url = image_uris.get("normal") if image_uris else None

                if image_url:
                    images_folder = "./images"
                    os.makedirs(images_folder, exist_ok=True)
                    
                    # Remove special characters from the filename
                    filename = re.sub(r'[^\w.-]', '', card_name)
                    filename = os.path.join(images_folder, f"magic_card_{filename}_{collector_number}.jpg")

                    if download_image(image_url, filename):
                        markdown_table += f" [![{alt_text}]({filename})]({scryfall_url}) |"
                else:
                    print(f"Image URL not found for {card_name}")
            else:
                print(f"Card '{card_name}' not found or no multiverseid available")

        markdown_table += "\n"

    return markdown_table

def process_batch(batch):
    batch_results = []

    for card_name in batch:
        card_data = find_card_by_name(card_name)
        if card_data:
            batch_results.append((card_name, card_data.get("set"), card_data.get("collector_number"), card_data))

    return batch_results

def generate_card_type_tables(card_data_list):
    card_type_tables = {}  # Dictionary to store tables for each card type

    for card_name, set_code, collector_number, card_data in card_data_list:
        type_line = card_data.get("type_line", "")
        simplified_type = re.split(r'\s*[-—]\s*', type_line, 1)[0].lower()  # Extract the part before the first hyphen or em dash

        card_type_tables.setdefault(simplified_type, []).append((card_name, set_code, collector_number, card_data))

    return card_type_tables

def print_card_type_tables(card_type_tables):
    for simplified_type, card_data_list in card_type_tables.items():
        print(f"\n## List of {' '.join(part.capitalize() for part in simplified_type.split('—')[0].strip().split())} cards ({len(card_data_list)})\n")
        markdown_table = generate_markdown_table(card_data_list)
        print(markdown_table)

def main():
    global verbose_output  # Declare global variable
    if len(sys.argv) < 2:
        print("Usage: ./scryfall_api_list_input.py <path_to_text_file> [--sort-by-type] [--verbose]")
        return

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    sort_by_type = "--sort-by-type" in sys.argv
    verbose_output = "--verbose" in sys.argv  # Set verbose_output based on command-line argument

    with open(file_path, 'r') as file:
        card_names = [line.strip() for line in file]

    card_data_list = []
    batch_size = 10

    # Use ThreadPoolExecutor to process cards concurrently in batches
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Split card_names into batches
        batches = [card_names[i:i+batch_size] for i in range(0, len(card_names), batch_size)]

        # Use tqdm to create a progress bar for concurrent processing
        futures = [executor.submit(process_batch, batch) for batch in tqdm(batches, desc="Processing Batches", unit="batch")]

        # Use as_completed to get results as threads finish
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing Results", unit="batch"):
            batch_results = future.result()
            card_data_list.extend(batch_results)

            # Introduce a delay between batches (e.g., 75 milliseconds)
            time.sleep(0.075)

    if sort_by_type:
        card_type_tables = generate_card_type_tables(card_data_list)
        print_card_type_tables(card_type_tables)
    else:
        markdown_table = generate_markdown_table(card_data_list)
        print("\nMarkdown Table:\n")
        print(markdown_table)

if __name__ == "__main__":
    main()
