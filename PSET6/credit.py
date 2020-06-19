from cs50 import get_int

def main():
    while True:
        number = get_int("Number: ")
        if number >= 0:
            break
    if(len(str(number)) == 15):
        if number//10e12 == 34 or number//10e12 == 37:
            print("AMEX")
            return
        else:
            print("Invalid")
            return

    if(len(str(number)) == 16):
        if number//10e13 in [51, 52, 53, 54, 55]:
            print("MasterCard")
            return
        elif number//10e14 == 4:
            print("Visa")
            return
        else:
            print("Invalid")
            return
    if(len(str(number)) == 13):
        if number//10e11 == 4:
            print("Visa")
            return
        else:
            print("Invalid")
            return
    else:
        print("Invalid")



main()