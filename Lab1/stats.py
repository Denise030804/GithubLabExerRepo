def mean(numbers):
    if len(numbers) == 0:
        return 0
    total = 0
    for num in numbers:
        total = total + num
    return total / len(numbers)

def median(numbers):
    if len(numbers) == 0:
        return 0
    sorted_numbers = sorted(numbers)
    length = len(sorted_numbers)
    if length % 2 == 0:
        middle1 = sorted_numbers[length // 2 - 1]
        middle2 = sorted_numbers[length // 2]
        return (middle1 + middle2) / 2
    else:
        return sorted_numbers[length // 2]

def mode(numbers):
    if len(numbers) == 0:
        return 0
    counts = {}
    for num in numbers:
        if num in counts:
            counts[num] = counts[num] + 1
        else:
            counts[num] = 1
    max_count = 0
    mode = 0
    for num, count in counts.items():
        if count > max_count:
            max_count = count
            mode = num
    return mode

def main():

    LIST = [15, 2, 10, 3, 18, 2, 6]
    print("Numbers:", LIST)
    print("Mean:", mean(LIST))
    print("Median:", median(LIST))
    print("Mode:", mode(LIST))

if __name__ == "__main__":
    main()