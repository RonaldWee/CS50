#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
//main


int main(void)
{
    string text = get_string("Text: ");
    int letters = 0, words = 1, sentences = 0;
    for (int i = 0, len = strlen(text); i < len ; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }

        if (text[i] == ' ' && text[i+1] != ' ')
        {
            words++;
        }

        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }

    }



    float L = letters / (float)words * 100;
    float S = sentences / (float)words * 100;

    int index = round((0.0588 * L) - (0.296 * S) - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }

}




