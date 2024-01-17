# MTG Markdown Decklist Generator

## Overview

This Python script generates a decklist in Markdown format using card data from the Scryfall API. It supports specifying commanders and sorting cards by type.

## Features

1. Card Data Retrieval
    - The script uses the Scryfall API to retrieve detailed information about Magic: The Gathering cards.

2. Image Download
    - Downloads card images from Scryfall based on the retrieved card data.

3. Markdown Decklist Generation
    - Generates a decklist in Markdown format.

4. Commander Support
    - Supports the specification of commander cards.
    - Commander cards are listed separately at the top of the generated decklist.

5. Type-based Sorting
    - Provides an option to sort cards by their types (e.g., creatures, artifacts, enchantments).

6. Verbose Output
    - Offers a `--verbose` option to enable detailed output during the script's execution.

7. Concurrent Processing:
    - Uses concurrent processing with `ThreadPoolExecutor` to speed up the retrieval of card data.

8. Progress Bar
    - Displays a progress bar using the tqdm library when processing batches.

9. Output to Markdown File
    - Can output the generated decklist as a Markdown file named `decklist.md`.

10. Customizable Desired Order
    - Allows defining a desired order for card types in the decklist.

11. Case-Insensitive Commander Matching
    - Ensures case-insensitive matching for commander names, avoiding issues with case discrepancies.

## Usage

### Prerequisites

- Python 3.x
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - tqdm

### Command-line Usage

```bash
./mtg_markdown_generator.py <path_to_text_file> [--sort-by-type] [--verbose] [--markdown] [--commander <commander_name(s)>]
```

- <path_to_text_file>: Path to a text file containing card names (one per line).
- --sort-by-type: Sort cards by type in the generated decklist.
- --verbose: Enable verbose output.
- --markdown: Output the decklist as a Markdown file (`decklist.md`).
- --commander <commander_name(s)>: Specify commander card(s) (separate multiple commanders with spaces).

### Example

```bash
./mtg_markdown_generator.py my_deck.txt --sort-by-type --verbose --markdown --commander "Krark, the Thumbless" "Kydele, Chosen of Kruphix" 
```

This example generates a decklist from my_deck.txt, sorting cards by type, including verbose output, specifying commanders "Krark, the Thumbless" and "Kydele, Chosen of Kruphix" and saving the result as `decklist.md`.

## Acknowledgments

- The script uses the Scryfall API for retrieving card data.
- tqdm is used for progress bars in concurrent processing.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
