#include "helpers.h"
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((float)(image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(0.393 * originalRed + 0.769 * originalGreen + 0.189 * originalBlue);
            int sepiaGreen = round(0.349 * originalRed + 0.686 * originalGreen + 0.168 * originalBlue);
            int sepiaBlue = round(0.272 * originalRed + 0.534 * originalGreen + 0.131 * originalBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;

        }
    }
    return;
}



// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < round(width / 2); j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }

    return;
}




// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE oimage[height][width];
    //duplicate
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            oimage[i][j] = image[i][j];
        }
    }
    //for those with 9
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            image[i][j].rgbtRed = round((float)(oimage[i - 1][j - 1].rgbtRed + oimage[i - 1][j].rgbtRed + oimage[i - 1][j + 1].rgbtRed + 
            oimage[i][j-1].rgbtRed + oimage[i][j].rgbtRed + oimage[i][j+1].rgbtRed + oimage[i+1][j-1].rgbtRed + oimage[i+1][j].rgbtRed + 
            oimage[i+1][j+1].rgbtRed) / 9);
            image[i][j].rgbtGreen = round((float)(oimage[i - 1][j - 1].rgbtGreen + oimage[i - 1][j].rgbtGreen + 
            oimage[i - 1][j + 1].rgbtGreen + oimage[i][j - 1].rgbtGreen + oimage[i][j].rgbtGreen + oimage[i][j + 1].rgbtGreen + 
            oimage[i + 1][j - 1].rgbtGreen + oimage[i + 1][j].rgbtGreen + oimage[i + 1][j + 1].rgbtGreen) / 9);
            image[i][j].rgbtBlue = round((float)(oimage[i - 1][j - 1].rgbtBlue + oimage[i - 1][j].rgbtBlue + 
            oimage[i - 1][j + 1].rgbtBlue + oimage[i][j - 1].rgbtBlue + oimage[i][j].rgbtBlue + oimage[i][j + 1].rgbtBlue + 
            oimage[i + 1][j - 1].rgbtBlue + oimage[i + 1][j].rgbtBlue + oimage[i + 1][j + 1].rgbtBlue) / 9);
        }
    }
    //for those with 6

    //1st row
    for (int i = 0; i < 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            image[i][j].rgbtRed = round((float)(oimage[i][j-1].rgbtRed + oimage[i][j].rgbtRed + oimage[i][j+1].rgbtRed + oimage[i+1][j-1].rgbtRed + oimage[i+1][j].rgbtRed + oimage[i+1][j+1].rgbtRed) / 6);
            image[i][j].rgbtGreen = round((float)(oimage[i][j-1].rgbtGreen + oimage[i][j].rgbtGreen + oimage[i][j+1].rgbtGreen + oimage[i+1][j-1].rgbtGreen + oimage[i+1][j].rgbtGreen + oimage[i+1][j+1].rgbtGreen) / 6);
            image[i][j].rgbtBlue = round((float)(oimage[i][j-1].rgbtBlue + oimage[i][j].rgbtBlue + oimage[i][j+1].rgbtBlue + oimage[i+1][j-1].rgbtBlue + oimage[i+1][j].rgbtBlue + oimage[i+1][j+1].rgbtBlue) / 6);
        }
    }
    //last row
    for (int i = height - 1; i <= height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            image[i][j].rgbtRed = round((float)(oimage[i][j-1].rgbtRed + oimage[i][j].rgbtRed + oimage[i][j+1].rgbtRed + oimage[i-1][j-1].rgbtRed + oimage[i-1][j].rgbtRed + oimage[i-1][j+1].rgbtRed) / 6);
            image[i][j].rgbtGreen = round((float)(oimage[i][j-1].rgbtGreen + oimage[i][j].rgbtGreen + oimage[i][j+1].rgbtGreen + oimage[i-1][j-1].rgbtGreen + oimage[i-1][j].rgbtGreen + oimage[i-1][j+1].rgbtGreen) / 6);
            image[i][j].rgbtBlue = round((float)(oimage[i][j-1].rgbtBlue + oimage[i][j].rgbtBlue + oimage[i][j+1].rgbtBlue + oimage[i-1][j-1].rgbtBlue + oimage[i-1][j].rgbtBlue + oimage[i-1][j+1].rgbtBlue) / 6);
        }
    }
    //first column
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 0; j < 1; j++)
        {
            image[i][j].rgbtRed = round((float)(oimage[i-1][j].rgbtRed + oimage[i-1][j+1].rgbtRed + oimage[i][j].rgbtRed + oimage[i][j+1].rgbtRed + oimage[i+1][j].rgbtRed + oimage[i+1][j+1].rgbtRed) / 6);
            image[i][j].rgbtGreen = round((float)(oimage[i-1][j].rgbtGreen + oimage[i-1][j+1].rgbtGreen + oimage[i][j].rgbtGreen + oimage[i][j+1].rgbtGreen + oimage[i+1][j].rgbtGreen + oimage[i+1][j+1].rgbtGreen) / 6);
            image[i][j].rgbtBlue = round((float)(oimage[i-1][j].rgbtBlue + oimage[i-1][j+1].rgbtBlue + oimage[i][j].rgbtBlue + oimage[i][j+1].rgbtBlue + oimage[i+1][j].rgbtBlue + oimage[i+1][j+1].rgbtBlue) / 6);

        }
    }
    //last column
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = width -1; j <= width -1; j++)
        {
            image[i][j].rgbtRed = round((float)(oimage[i-1][j].rgbtRed + oimage[i-1][j-1].rgbtRed + oimage[i][j].rgbtRed + oimage[i][j-1].rgbtRed + oimage[i+1][j].rgbtRed + oimage[i+1][j-1].rgbtRed) / 6);
            image[i][j].rgbtGreen = round((float)(oimage[i-1][j].rgbtGreen + oimage[i-1][j-1].rgbtGreen + oimage[i][j].rgbtGreen + oimage[i][j-1].rgbtGreen + oimage[i+1][j].rgbtGreen + oimage[i+1][j-1].rgbtGreen) / 6);
            image[i][j].rgbtBlue = round((float)(oimage[i-1][j].rgbtBlue + oimage[i-1][j-1].rgbtBlue + oimage[i][j].rgbtBlue + oimage[i][j-1].rgbtBlue + oimage[i+1][j].rgbtBlue + oimage[i+1][j-1].rgbtBlue) / 6);
        }
    }

    //for corners

    //topleft
    image[0][0].rgbtRed = round((float)(oimage[0][0].rgbtRed + oimage[0][1].rgbtRed + oimage[1][0].rgbtRed + oimage[1][1].rgbtRed) / 4);
    image[0][0].rgbtGreen = round((float)(oimage[0][0].rgbtGreen + oimage[0][1].rgbtGreen + oimage[1][0].rgbtGreen + oimage[1][1].rgbtGreen) / 4);
    image[0][0].rgbtBlue = round((float)(oimage[0][0].rgbtBlue + oimage[0][1].rgbtBlue + oimage[1][0].rgbtBlue + oimage[1][1].rgbtBlue) / 4);
    //topright
    image[0][width-1].rgbtRed = round((float)(oimage[0][width-1].rgbtRed + oimage[0][width-2].rgbtRed + oimage[1][width-1].rgbtRed + oimage[1][width-2].rgbtRed) / 4);
    image[0][width-1].rgbtGreen = round((float)(oimage[0][width-1].rgbtGreen + oimage[0][width-2].rgbtGreen + oimage[1][width-1].rgbtGreen + oimage[1][width-2].rgbtGreen) / 4);
    image[0][width-1].rgbtBlue = round((float)(oimage[0][width-1].rgbtBlue + oimage[0][width-2].rgbtBlue + oimage[1][width-1].rgbtBlue + oimage[1][width-2].rgbtBlue) / 4);
    //btmleft
    image[height-1][0].rgbtRed = round((float)(oimage[height-1][0].rgbtRed + oimage[height-1][1].rgbtRed + oimage[height-2][0].rgbtRed + oimage[height-2][1].rgbtRed) / 4);
    image[height-1][0].rgbtGreen = round((float)(oimage[height-1][0].rgbtGreen + oimage[height-1][1].rgbtGreen + oimage[height-2][0].rgbtGreen + oimage[height-2][1].rgbtGreen) / 4);
    image[height-1][0].rgbtBlue = round((float)(oimage[height-1][0].rgbtBlue + oimage[height-1][1].rgbtBlue + oimage[height-2][0].rgbtBlue + oimage[height-2][1].rgbtBlue) / 4);
    //btmright
    image[height-1][width-1].rgbtRed = round((float)(oimage[height-1][width-1].rgbtRed + oimage[height-1][width-2].rgbtRed + oimage[height-2][width-1].rgbtRed + oimage[height-2][width-2].rgbtRed) / 4);
    image[height-1][width-1].rgbtGreen = round((float)(oimage[height-1][width-1].rgbtGreen + oimage[height-1][width-2].rgbtGreen + oimage[height-2][width-1].rgbtGreen + oimage[height-2][width-2].rgbtGreen) / 4);
    image[height-1][width-1].rgbtBlue = round((float)(oimage[height-1][width-1].rgbtBlue + oimage[height-1][width-2].rgbtBlue + oimage[height-2][width-1].rgbtBlue + oimage[height-2][width-2].rgbtBlue) / 4);


    return;
}
