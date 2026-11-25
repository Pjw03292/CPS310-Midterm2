# CPS 310 Midterm 2 — Zombie Game Simulation Framework

**Name:** Patrick Williams

## Simulation design

The simulation tracks three character states: `human`, `infected`, and `zombie`. Each tick takes a list of events. In this project, a `bite` event means the named character receives a bite. A human who receives a bite becomes infected. On a later tick, a `turn` event can change that infected character into a zombie. Each character can receive at most one event per tick.

The ontology in `ontology.json` defines the states, the events allowed in each state, the state that results from each event, and the event limit per tick. For example, `bite` is allowed for humans and leads to `infected`. The `turn` event is allowed for infected characters and leads to `zombie`.

## AI development pipeline

1. **Define the game rules.** Specify the character states, which events each state allows, and what should happen when a tick contains an invalid event.
2. **Represent the rules in an ontology.** Put the allowed transitions and event limit in `ontology.json` so they can be reviewed directly against the game rules.
3. **Use AI to develop the simulation.** Build `simulation.py` around a `step` function that reads the rules from the ontology. The function checks character names, the event limit, and whether each event is allowed for the character's current state.
4. **Run the demo cases.** Check that a human can become infected and turn on a later tick. Also check that the simulation rejects a bite event for a zombie and rejects a bite and turn for the same character in one tick.
5. **Generate and test a baseline.** Give AI the same gameplay rules in plain English. Save the generated function in `baseline.py` and use `compare_baseline.py` to run the same scenarios.
6. **Record the evidence.** Save the terminal output in `demo-results.txt` and the prompts in `prompts.md`.

## Why the controls work

The ontology controls which events can change each character's state. For example, the zombie rules contain no `bite` transition, so the simulation rejects a bite event for a zombie. The one-event limit controls the order of changes across ticks. It prevents a human from receiving a bite and turning into a zombie in the same tick.

The function applies changes to a copy of the starting states. If a tick fails midway through processing, the caller's original dictionary is preserved. The demo checks this behavior for the rejected cases.

Keeping the rules in `ontology.json` also makes them easier to review before running the simulation. A reviewer can find the allowed events for each state in one place and check them against the requirements. A change to an existing transition can be made in the JSON and then checked by rerunning the demos.

## Demo results and baseline comparison

Both versions produced the same results for the scenarios I ran.

| Scenario | Ontology-driven version | Baseline |
| --- | --- | --- |
| Alex receives a bite while Sam moves | Alex becomes infected and Sam stays a zombie | Same result |
| Alex turns on the next tick | Alex becomes a zombie | Same result |
| Sam receives a bite while already a zombie | Event rejected and starting state preserved | Same result |
| Alex receives a bite and turns in the same tick | Tick rejected and starting state preserved | Same result |

The baseline generated from the plain-English rules passed every case. For these scenarios, the two approaches had the same behavior. The difference is how the rules are reviewed and updated. In the ontology-driven version, the transition rules are in `ontology.json`. In the baseline, those rules are in `baseline.py`, so changing a transition requires editing the Python file. The terminal output is saved in `demo-results.txt`.

## How to run

Open a terminal in the project folder and run:

```powershell
python simulation.py
python compare_baseline.py
```

The first command runs the ontology-driven demo. The second runs the same scenarios using the baseline.