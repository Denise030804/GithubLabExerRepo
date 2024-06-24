import os

def read_file_to_list(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return lines

def navigate_lines(filename):
    try:
        lines = read_file_to_list(filename)
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
        return
    
    num_lines = len(lines)
    print(f"The file '{filename}' contains {num_lines} lines.")
    
    while True:
        try:
            line_number = int(input(f"Enter a line number (1-{num_lines}) or 0 to quit: "))
            if line_number == 0:
                print("Exiting the program.")
                break
            elif 1 <= line_number <= num_lines:
                print(f"Line {line_number}: {lines[line_number - 1].strip()}")
            else:
                print(f"Please enter a valid line number between 1 and {num_lines}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    filename = input("Enter the filename: ")
    navigate_lines(filename)
