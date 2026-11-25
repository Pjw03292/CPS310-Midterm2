from baseline import step

start = {"Alex": "human", "Sam": "zombie"}

first = step(start, [("Alex", "bite"), ("Sam", "move")])
print("Tick 1:", first)
print("Tick 2:", step(first, [("Alex", "turn")]))

for events in [[("Sam", "bite")], [("Alex", "bite"), ("Alex", "turn")]]:
    original = start.copy()
    try:
        result = step(original, events)
    except ValueError as error:
        print("Rejected:", error)
    else:
        print("Accepted:", result)
    print("Original state preserved:", original == start)