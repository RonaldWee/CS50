from cs50 import get_string

def main():
    text = get_string("Text: ")
    letters = 0
    words = 1
    sentences = 0
    for char in range(len(text)):
        if text[char].isalpha():
            letters += 1
        if text[char] == ' ' and text[char+1] != ' ':
            words += 1
        if text[char] == '.' or text[char] == '?' or text[char] == '!':
            sentences += 1

    L = float(letters) / float(words) * 100
    S = float(sentences) / float(words) * 100

    grade = round(0.0588 * L - 0.296 * S - 15.8)
    if grade < 1:
        print("Before Grade 1")
    elif grade >16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")
main()