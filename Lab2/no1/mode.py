def mode(numbers):
    if not numbers:
        return 0
    # Convert numbers to strings for consistency with the original mode.py
    words = [str(num).upper() for num in numbers]
    theDictionary = {}
    for word in words:
        number = theDictionary.get(word, None)
        if number == None:
            theDictionary[word] = 1
        else:
            theDictionary[word] = number + 1
    theMaximum = max(theDictionary.values())
    for key in theDictionary:
        if theDictionary[key] == theMaximum:
            return float(key)  # Convert back to float before returning