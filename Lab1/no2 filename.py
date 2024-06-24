def read_file(filename):
    """Read the contents of a file into a list of lines."""
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except IOError:
        print(f"Error: There was an issue reading the file '{filename}'.")
        return None

def display_line(lines, line_number):
    """Display a specific line from the list of lines."""
    if 1 <= line_number <= len(lines):
        print(f"Line {line_number}: {lines[line_number-1].strip()}")
    else:
        print(f"Error: Line number {line_number} is out of range.")

def main():
    filename = input("Enter the filename: ")
    lines = read_file(filename)
    
    if lines is None:
        return

    while True:
        print(f"\nThe file has {len(lines)} lines.")
        try:
            line_number = int(input("Enter a line number (0 to quit): "))
            if line_number == 0:
                print("Exiting the program. Goodbye!")
                break
            display_line(lines, line_number)
        except ValueError:
            print("Error: Please enter a valid integer.")

if __name__ == "__main__":
    main()