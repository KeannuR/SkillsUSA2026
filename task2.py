from collections import deque

def seat_allocation(n: int, arr: list[int]) -> list[int]:
    #(original_index, preferred_seat)
    queue = deque((i, arr[i]) for i in range(n))
    #track occupied seats
    occupied = set()
    
    result = [0] * n
    #process until everyone gets a seat
    while queue:
        person, preferred = queue.popleft()

        if preferred not in occupied:
            #assign seat
            occupied.add(preferred)
            result[person] = preferred
        else:
            #bump seat by 1 and rejoin que
            queue.append((person, preferred + 1))
    return result


if __name__ == "__main__":
   seat_allocation(5, 1,2,3,5,4)

