# MTG Markdown Generator

A Python script to generate markdown tables for Magic: The Gathering cards using the Scryfall API.

## Overview

This script takes a list of Magic: The Gathering card names, queries the Scryfall API for card information, and generates markdown tables for easy inclusion in your project, documentation, or website.

## Features

- **Card Information:** Retrieve detailed information for each card, including set code, collector number, and image download.
- **Markdown Tables:** Generate markdown tables organized by card type, making it easy to display cards in your preferred format.
- **Batch Processing:** Efficiently process large lists of cards in batches, avoiding rate limits and improving performance.

## Usage

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/mtg-scryfall-api-card-list.git
   cd mtg-scryfall-api-card-list
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Create Input File:**

Create a text file (e.g., `input.txt`) with each line containing a Magic: The Gathering card name.

4. **Run the Script:**

    ```bsh
    ./scryfall_api_list_input.py input.txt --sort-by-type
    ```

- Use `--sort-by-type` to organize cards by type.
- Use `--verbose for` detailed output.

5. **Output:**

The script will generate markdown tables that can be copy+pasted into documents and downloads card images into the `images/` folder.

## Contributing

Contributions are welcome! If you have suggestions, bug reports, or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
