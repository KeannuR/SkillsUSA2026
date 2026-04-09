import sys

from task1 import text_editor_backspace as solution1
from task2 import seat_allocation as solution2
from task3 import init as solution3


def main():
   

    task = sys.argv[1]
    print((f"Task {task}:" ))
    args = sys.argv[2:]
    if task == "1":
        if len(args) != 2:
            print("Task 1 requires 2 arguments")
            return

        result = solution1(args[0], args[1])
        print(result)

    elif task == "2":
        def format_to_list(input_string : str):
            return list(map(int, input_string.split(',')))
        result = solution2(int(args[0]), format_to_list(args[1]))
        print(result)
    elif task == "3":
        solution3()

    else:
        print("Invalid task number")


if __name__ == "__main__":
    main()