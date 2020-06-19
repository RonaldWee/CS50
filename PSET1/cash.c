#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Dollars: ");
    } while (dollars <= 0);

    int cents = round(dollars * 100);

    int coins = 0;

    while(cents >= 25)
    {
        coins += 1;
        cents -= 25;
    }
    while(cents < 25 && cents >= 10)
    {
        coins += 1;
        cents -=10;
    }
    while(cents < 10 && cents >= 5)
    {
        coins += 1;
        cents -= 5;
    }
    while(cents <5 && cents >0)
    {
        coins += 1;
        cents -= 1;
    }
    printf("%i\n", coins);
}