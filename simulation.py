import json
from collections import Counter
from pathlib import Path

with Path(__file__).with_name("ontology.json").open(encoding="utf-8") as file:
    ONTOLOGY = json.load(file)


def step(agents, events):
    """Apply one tick and return the updated states."""
    updated = dict(agents)
    counts = Counter(actor for actor, _ in events)

    for actor, event in events:
        if actor not in agents:
            raise ValueError(f"Unknown actor: {actor}")
        if counts[actor] > ONTOLOGY["max_events_per_actor_per_tick"]:
            raise ValueError(f"Multiple events for {actor}")

        state = agents[actor]
        transitions = ONTOLOGY["states"][state]
        if event not in transitions:
            raise ValueError(f"Illegal transition: {state} + {event}")

        updated[actor] = transitions[event]

    return updated


if __name__ == "__main__":
    start = {"Alex": "human", "Sam": "zombie"}

    first = step(start, [("Alex", "bite"), ("Sam", "move")])
    second = step(first, [("Alex", "turn")])
    assert first == {"Alex": "infected", "Sam": "zombie"}
    assert second == {"Alex": "zombie", "Sam": "zombie"}
    print("Tick 1:", first)
    print("Tick 2:", second)

    bad_cases = [
        ([("Sam", "bite")], "Illegal transition: zombie + bite"),
        ([("Alex", "bite"), ("Alex", "turn")], "Multiple events for Alex"),
    ]
    for events, expected_error in bad_cases:
        try:
            step(start, events)
        except ValueError as error:
            assert str(error) == expected_error
            assert start == {"Alex": "human", "Sam": "zombie"}
            print("Rejected:", error)
        else:
            raise AssertionError(f"Expected rejection for {events}")