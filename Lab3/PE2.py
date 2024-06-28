import random
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
        return sum(self.scores) / len(self._scores)
    
    def getHighScore(self):
        return max(self.scores)
    
    def __eq__(self,student):
        return self.name == student.name
  
    def __ge__(self,student):
        return self.name == student.name or self.name>student.name
  
    def __lt__(self,student):
        return self.name<student.name
 
    def __str__(self):
        return "Name: " + self.name  + "\nScores: " + \
               " ".join(map(str, self.scores))

def main():
    
    studentlist = [
        Student("Alice", 5),
        Student("Bob", 5),
        Student("Charlie", 5),
        Student("David", 5),
        Student("Eve", 5)
    ]
  
    random.shuffle(studentlist)
    print("\n\nUnsorted list of students:")
    for student in studentlist:
        print(student)
    
    studentlist.sort()
    print("\n\nSorted list of students: ")
    for student in studentlist:
        print(student)

if __name__ == "__main__":
    main()


