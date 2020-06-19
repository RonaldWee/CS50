import csv
from sys import argv, exit
from cs50 import SQL

def main():
    if len(argv) != 2:
        print("Error")
        exit(1)
    db = SQL("sqlite:///students.db")


    with open(argv[1], "r") as characters:
        reader = csv.DictReader(characters)
        for row in reader:
            names = []
            for part in row["name"].split(" "):
                names.append(part)
            names.append(row["house"])
            names.append(row["birth"])
            row['name'].split(" ")
            if len(names) == 5:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", names[0:5])
            if len(names) == 4:
                db.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)", names[0:4])
main()





