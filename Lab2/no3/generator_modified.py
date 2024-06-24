import os
import random

def getWords(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    with open(file_path, 'r') as file:
        words = file.read().split()
    return tuple(words)


def sentence():
    return nounPhrase() + " " + verbPhrase()

def nounPhrase():
    return random.choice(getWords('articles.txt')) + " " + random.choice(getWords('nouns.txt'))

def verbPhrase():
    return random.choice(getWords('verbs.txt')) + " " + nounPhrase() + " " + \
           prepositionalPhrase()

def prepositionalPhrase():
    return random.choice(getWords('prepositions.txt')) + " " + nounPhrase()

def main():
    
    number = int(input("Enter the number of sentences: "))
    for count in range(number):
        print(sentence())


if __name__ == "__main__":
    main()
