import csv
from sys import argv, exit
from cs50 import SQL

def main():
    if len(argv) != 2:
        print("Error")
        exit(1)

    db = SQL("sqlite:///students.db")

    search = db.execute(f"SELECT first,middle,last,birth FROM students WHERE house = '{argv[1]}' ORDER BY last, first")
    for i in range(len(search)):
        if search[i]['middle'] == None:
            print(f"{search[i]['first']} {search[i]['last']}, born {search[i]['birth']}")
        else:
            print(f"{search[i]['first']} {search[i]['middle']} {search[i]['last']}, born {search[i]['birth']}")
main()

