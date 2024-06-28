class Student(object):
    def __init__(self, name, number):
        self.name = name
        self.scores = []
        for count in range(number):
            self.scores.append(0)

    def getName(self):
        return self.name
  
    def setScore(self, i, score):
        self.scores[i - 1] = score

    def getScore(self, i):
        return self.scores[i - 1]
   
    def getAverage(self):
        return sum(self.scores) / len(self.scores)
    
    def getHighScore(self):
        return max(self.scores)
 
    def __str__(self):
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __ge__(self, other):
        return self.name >= other.name

def main():
    print("Students:" )
    print("Dale")
    print("Ciel")
    print("Azkael")
    print("Results:")
    
    student1 = Student("Dale",2)
    student2 = Student("Ciel",6)
    student3 = Student("Azkiel",6)
    
    print("Testing equality:")
    print(f"{student1.getName()} == {student2.getName()}: {student1 == student2}")
    print(f"{student1.getName()} == {student3.getName()}: {student1 == student3}")

    print("\nTesting less than:")
    print(f"{student1.getName()} < {student2.getName()}: {student1 < student2}")
    print(f"{student2.getName()} < {student1.getName()}: {student2 < student1}")

    print("\nTesting greater than or equal to:")
    print(f"{student1.getName()} >= {student2.getName()}: {student1 >= student2}")
    print(f"{student2.getName()} >= {student1.getName()}: {student2 >= student1}")
    print(f"{student1.getName()} >= {student3.getName()}: {student1 >= student3}")

if __name__ == "__main__":
    main()