import os
import json

def main():
    input_file = "dataset_middle.txt"
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # Split the input into blocks separated by blank lines.
    blocks = [block.strip() for block in content.split("\n\n") if block.strip()]
    
    problems_dir = "problems"
    solutions_dir = "solutions"
    
    # Create directories if they don't exist.
    os.makedirs(problems_dir, exist_ok=True)
    os.makedirs(solutions_dir, exist_ok=True)
    
    for block in blocks:
        try:
            data = json.loads(block)
        except Exception as e:
            print(f"Error parsing block: {e}")
            continue
        
        # Build problem and solution dictionaries.
        problem = {
            "problem_id": data.get("problem_id", ""),
            "initial_string": data.get("initial_string", ""),
            "transitions": data.get("transitions", [])
        }
        solution = {
            "problem_id": data.get("problem_id", ""),
            "solution": data.get("solution", "")
        }
        
        filename = f"{data.get('problem_id', 'unknown')}.json"
        with open(os.path.join(problems_dir, filename), 'w') as pf:
            json.dump(problem, pf, indent=4)
        with open(os.path.join(solutions_dir, filename), 'w') as sf:
            json.dump(solution, sf, indent=4)

if __name__ == "__main__":
    main()