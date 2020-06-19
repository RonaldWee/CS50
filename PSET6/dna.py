from sys import argv, exit
import csv
from cs50 import get_string

def main():
    #ensure user inputs correctly
    if len(argv) != 3:
        print("missing command-line argument")
        exit(1)

    #read individual dna from file
    with open(argv[2]) as file:
        individual = csv.reader(file)
        for row in individual:
            individual_dna = row
    #store it
    dna = individual_dna[0]

    #dictionary for the different types of STR
    sequences = {}

    #extract STR from database
    with open(argv[1], 'r') as file:
        people = csv.reader(file)
        for row in people:
            dnaSequences = row
            dnaSequences.pop(0)
            break

    #make the different STR into a dict, with values(counter) = 0
    for item in dnaSequences:
        sequences[item] = 0


    for key in sequences:
        length = len(key)
        Maxcount = 0
        count = 0
        for i in range(len(dna)):
            #reset temp to 0
            while count > 0:
                count -= 1
                continue
            #find number of consecutive counts
            if dna[i:i + length] == key:
                while dna[i - length: i] == dna[i: i + length]:
                    count += 1
                    i += length
                #replace Maxcount with count if count is more than Maxcount
                if count > Maxcount:
                    Maxcount = count

        sequences[key] += Maxcount + 1

    #open database and find if the number of STR matches the STR count in sequences
    with open(argv[1],'r') as file:
        namelist = csv.DictReader(file)
        for name in namelist:
            match = 0
            for dna in sequences:
                #if 1 STR count matches
                if sequences[dna] == int(name[dna]):
                    match += 1
                #if everything matches
                if match == len(sequences):
                    print(name['name'])
                    exit()

        print('No match')



main()