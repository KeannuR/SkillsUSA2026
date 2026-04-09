from collections import deque

def seat_allocation(n: int, arr: list[int]) -> list[int]:
    # Queue stores (original_index, preferred_seat)
    queue = deque((i, arr[i]) for i in range(n))
    
    occupied = set()
    result = [0] * n

    while queue:
        person, preferred = queue.popleft()

        if preferred not in occupied:
            occupied.add(preferred)
            result[person] = preferred
        else:
            # Bump preferred seat by 1 and rejoin the back of the queue
            queue.append((person, preferred + 1))

    return result


if __name__ == "__main__":
    print(seat_allocation(5, [1, 2, 3, 2, 4]))  # [1, 2, 3, 5, 4]
    print(seat_allocation(3, [1, 1, 1]))          # [1, 2, 3]
    print(seat_allocation(4, [3, 3, 3, 3]))       # [3, 4, 5, 6]