BACKSPACE = "#"


def backspace(s: str) -> str:
    """
    Processes a string where '#' acts like a backspace.
    Returns the final edited string.
    """
    result = []
    skip = 0
    index = len(s) - 1  # Start from the end 

    # Right to left of the string
    while index >= 0:
        char = s[index]

        if char == BACKSPACE:
            skip += 1
        elif skip > 0:
            skip -= 1
        else:
            result.append(char)  # Append kept characters

        index -= 1
    #reverse since characters were collected right to left 
    return "".join(reversed(result))

#pointer from right to left
def backspace(s: str) -> str:
    result = ""
    skip = 0
    index = len(s) - 1

    while index >= 0:
        char = s[index]
        if char == BACKSPACE:
            skip += 1
        elif skip > 0:
            skip -= 1
        else:
            result = char + result 
        index -= 1

    return result
    




def text_editor_backspace(string1, string2) -> bool:
    if backspace(string1) == backspace(string2): return True
    return False



if __name__ == "__main__":
    print(text_editor_backspace("H#allo", "H#ello"))