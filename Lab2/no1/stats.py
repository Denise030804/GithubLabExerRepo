from mean import mean
from median import median
from mode import mode

def main():
    input_string = input("Enter some numbers: ")
    number_strings = input_string.split()
    numbers = [float(num_str) for num_str in number_strings]
    
    print(f"Mean: {mean(numbers)}")
    print(f"Median: {median(numbers)}")
    print(f"Mode: {mode(numbers)}")

if __name__ == "__main__":
    main()