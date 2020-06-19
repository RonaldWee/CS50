from cs50 import get_float

def main():
    while True:
        change = get_float("Change owed: ")
        if change >= 0:
            break
    change = change * 100
    coins = 0
    while change >= 25:
        coins += 1
        change -= 25
    while change < 25 and change >= 10:
        coins += 1
        change -= 10
    while change < 10 and change >= 5:
        coins += 1
        change -= 5
    while change <5 and change >0:
        coins += 1
        change -= 1
    print(coins)
main()


