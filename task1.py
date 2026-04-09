BACKSPACE = "#"


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