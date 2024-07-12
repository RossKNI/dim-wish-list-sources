import re

# Define function to read search terms from file
def load_search_terms(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        search_terms = [line.strip() for line in file if line.strip()]
    return search_terms

# Define function to remove code blocks containing any search term
def remove_code_blocks(input_file, search_terms):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = []
    skip_block = False

    for line in lines:
        if skip_block:
            # Check if we have reached the end of the block
            if line.strip() == "":
                skip_block = False
            continue

        # Check if line contains any search term
        if any(term in line for term in search_terms):
            skip_block = True
            continue
        
        output_lines.append(line)

    with open(input_file, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

# Main script execution with error handling
try:
    # Load search terms
    search_terms = load_search_terms('SearchTermRemovals.txt')

    # Remove code blocks from file
    remove_code_blocks('RauceWishList.txt', search_terms)
    print("Processing completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Wait for user input before closing
input("Press Enter to exit...")
