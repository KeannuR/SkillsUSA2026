# REFER TO README :)

import sys

from task1 import text_editor_backspace as solution1
from task2 import seat_allocation as solution2
from task3 import init as solution3


def main():
   

    task = sys.argv[1]
    args = sys.argv[2:]

    print((f"Task {task}:" ))

#-------

    if task == "1":
        #data validation
        if len(args) != 2:
            print("Task 1 requires 2 arguments")
            print("Ex. python3 main.py 1 hello h#llo")
            return

        result = solution1(args[0], args[1])
        #result
        print(result)

#-------
    elif task == "2":
        #data validation 
        if len(args) != 2:
            print("Error: Task 2 requires exactly 2 arguments.")
            print("Example: python3 main.py 2 5 1,2,3,2,4")
            return
        
        try:
            n = int(args[0])
            if n <= 0:
                print("Error: n must be a positive integer.")
                return
        except ValueError:
            print("Error: n must be an integer.")
            return
        
        def format_to_list(input_string : str):
            return list(map(int, input_string.split(',')))
        # make sure only ints in list
        try:
            formattedList = format_to_list(args[1])
        except (ValueError, TypeError):
            print("Only ints in list")
            return False

        if len(formattedList) != n:
            print("The length of the list must be equal to the the first argument")
            return
        result = solution2(n, format_to_list(args[1]))
        #result
        print(result)
#-------

    elif task == "3":
        solution3()

    else:
        print("Invalid task number")


if __name__ == "__main__":
    main()