from cs50 import get_int

def main():
    height = get_int("Height: ")
    if height >= 1 and height <=8:
        for i in range(height):
            print(" " * (height-i-1) + "#" * (i+1) + "  " + "#" * (i+1))

    else:
        main()


main()

