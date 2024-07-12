import re

# Define function to find the starting line in large file
def find_starting_line(input_file, start_phrase):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if start_phrase in line:
                return i
    return -1  # Return -1 if start phrase is not found

# Define function to read search terms from file
def load_search_terms(filename):
    search_terms = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # If there's a comment, take only the part before the comment
            if '//' in line:
                line = line.split('//')[0].strip()
            
            # If the line starts with a number, take only the number
            if line and line[0].isdigit():
                line = re.match(r'\d+', line).group()
            
            if line:
                search_terms.append(line)

    return search_terms

# Define function to remove code blocks containing any search term
def remove_code_blocks(input_file, search_terms, start_phrase):
    # Find the index of starting line to begin removal
    start_index = find_starting_line(input_file, start_phrase)
    if start_index == -1:
        print(f"Error: '{start_phrase}' not found in '{input_file}'.")
        return
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    output_lines = lines[:start_index]  # Include lines before start phrase
    skip_block = False

    for line in lines[start_index:]:
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
    start_phrase = "Standard DIM community wishlist"
    
    # Load search terms
    search_terms = load_search_terms('SearchTermRemovals.txt')

    # Remove code blocks from file
    remove_code_blocks('RauceWishList.txt', search_terms, start_phrase)
    print("Processing completed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")

# Wait for user input before closing
input("Press Enter to exit...")
