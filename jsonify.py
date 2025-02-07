import os
import sys
import json
import re

def parse_transition(line):
    # Extract two strings between quotes.
    matches = re.findall(r'"(.*?)"', line)
    if len(matches) != 2:
        raise ValueError("Transition line doesn't have two quoted strings")
    return {"src": matches[0], "tgt": matches[1]}

def process_block(lines, problem_id):
    # First line: number of transitions.
    n = int(lines[0])
    transitions = []
    for i in range(1, n+1):
        transitions.append(parse_transition(lines[i]))
    initial_string = lines[n+1].strip()
    number_seq = lines[n+2].strip()
    # Reverse the number sequence and convert to list of integers.
    solution = [int(d) for d in number_seq[::-1]]
    
    problem_data = {
        "problem_id": "{:03}".format(problem_id),
        "initial_string": initial_string,
        "transitions": transitions
    }
    solution_data = {
        "problem_id": "{:03}".format(problem_id),
        "solution": solution
    }
    return problem_data, solution_data

def main():
    with open(sys.argv[1], 'r') as f:
        content = f.read()

    # Split data on blank lines.
    blocks = [block.strip() for block in content.strip().split("\n\n") if block.strip()]
    
    problems_dir = "problems"
    solutions_dir = "solutions"
    
    current_id = 0
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 4:
            continue  # Skip invalid blocks.
        problem_data, solution_data = process_block(lines, current_id)
        filename = "{:03}.json".format(current_id)
        with open(os.path.join(problems_dir, filename), 'w') as pf:
            json.dump(problem_data, pf, indent=4)
        with open(os.path.join(solutions_dir, filename), 'w') as sf:
            json.dump(solution_data, sf, indent=4)
        current_id += 1

if __name__ == "__main__":
    main()