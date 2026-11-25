def step(agents, events):
    transitions = {
        "human": {"wait": "human", "move": "human", "bite": "infected"},
        "infected": {"wait": "infected", "turn": "zombie"},
        "zombie": {"wait": "zombie", "move": "zombie"},
    }

    next_agents = dict(agents)
    seen = set()

    for actor, event in events:
        if actor not in agents:
            raise ValueError(f"Unknown actor: {actor}")
        if actor in seen:
            raise ValueError(f"Multiple events for {actor}")

        state = agents[actor]
        allowed = transitions.get(state, {})
        if event not in allowed:
            raise ValueError(f"Illegal transition: {state} + {event}")

        next_agents[actor] = allowed[event]
        seen.add(actor)

    return next_agents