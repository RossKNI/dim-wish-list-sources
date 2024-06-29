import re
import sys

def load_search_terms(file_path):
    try:
        search_terms = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Ignore the rest of the line if it starts with a number
                    match = re.match(r'^\d+', line)
                    if match:
                        term = match.group()
                        search_terms.append(term)
                    else:
                        search_terms.append(line)
        return search_terms
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{file_path}': {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def remove_blocks(input_file, search_terms_file):
    search_terms = load_search_terms(search_terms_file)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{input_file}': {e}")
        input("Press Enter to exit...")
        sys.exit(1)

    output_lines = []
    deleted_lines = []
    skip_block = False

    try:
        for line in lines:
            if skip_block:
                if line.strip() == "":  # Blank line indicates end of block
                    skip_block = False
                    deleted_lines.append(line)
                else:
                    deleted_lines.append(line)
                    continue
            else:
                matched = False
                for term in search_terms:
                    if term in line.strip():
                        skip_block = True
                        matched = True
                        deleted_lines.append(line)
                        break
                if not matched:
                    output_lines.append(line)
        
        with open(input_file, 'w', encoding='utf-8') as file:
            file.writelines(output_lines)
        
        # Display the deleted lines
        print("Deleted lines:")
        for line in deleted_lines:
            print(line.strip())
        
    except Exception as e:
        print(f"An unexpected error occurred while processing the file: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    input_file = "RauceWishList.txt"
    search_terms_file = "SearchTermRemovals.txt"
    try:
        remove_blocks(input_file, search_terms_file)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")

    print("Processing completed successfully.")
    input("Press Enter to exit...")
