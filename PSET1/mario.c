#include <stdio.h>
#include <cs50.h>

int main(void)
{

    int height;
    do
    {
        height = get_int("Height: ");
    } while (height > 8 || height <1);

    for (int row = 0; row < height; row++)
    {
        for (int space = height -1; space >= row+1; space--)
            printf(" ");

        for (int hash = 1; hash <= row+1; hash++)
            printf("#");

        printf("\n");

    }
}




