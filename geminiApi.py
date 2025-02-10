import json
import argparse
from google import genai
from pydantic import BaseModel
import time

class PuzzleAnswer(BaseModel):
    explanation: str
    solvable: str
    solution: str


def call_gemini_api(prompt, temperature, top_p, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            'temperature': temperature,
            'top_p': top_p,
            'response_mime_type': 'application/json',
            'response_schema': PuzzleAnswer  # Use PuzzleAnswer as the response schema
        }
    )
    return response

def generate_prompts_from_dataset(file_path, id_start, id_end):
    prompts = []  # List to hold generated prompt strings.
    initial_strings = []
    transitionList = []
    with open(file_path, 'r') as f:
        content = f.read()
        # Assume each JSON object is separated by blank lines.
        blocks = [block.strip() for block in content.split('\n\n') if block.strip()]
        for block in blocks:
            try:
                # Load each block as a JSON object.
                data = json.loads(block)
                pid = int(data.get("problem_id", -1))
                if id_start <= pid <= id_end:
                    initial = data.get("initial_string", "")
                    transitions = data.get("transitions", [])
                    transitions_str = ""
                    # CHANGED: Build the transitions part as required.
                    for transition in transitions:
                        src = transition.get("src", "")
                        tgt = transition.get("tgt", "")
                        transitions_str += f'"{src}"->"{tgt}"\n'
                    #Zero-Shot
                    # prompt_text = (
                    #     "Here is a puzzle: \n"
                    #     "You start with an initial string and you are given a set of transitions. During a single transition, you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.\n"
                    #     "Solve this problem:\n"
                    #     f"initial string: {initial}\n"
                    #     "transitions:\n"
                    #     f"{transitions_str}"
                    #     "//transitions end here\n"
                    #     "write a full solution with explanation of each step in the explanation field.\n"
                    #     "Explain if you think the problem is solvable by responding with \"yes or \"no in the solvable field.\n"
                    #     "The solution field should have an array of the indices of the rules you used in the solution (0 indexed from the top). Eg:[0,2,1](illustrative example)\n"
                    # )

                    #1-shot
                    # prompt_text = (
                    #     "Here is a puzzle: \n"
                    #     "You start with an initial string and you are given a set of transitions. During a single transition, you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.\n"
                    #     "Solve this problem:\n"
                    #     f"initial string: {initial}\n"
                    #     "transitions:\n"
                    #     f"{transitions_str}"
                    #     "//transitions ends here\n"
                    #     "write a full solution with explanation of each step in the explanation field.\n"
                    #     "Explain if you think the problem is solvable by responding with \"yes or \"no in the solvable field.\n"
                    #     "The solution field should have an array of the indices of the rules you used in the solution (0 indexed from the top). Eg:[0,2,1](illustrative example)\n"
                    #     "Here is an example:\n"
                    #     "initial string: 1cdAml8\n"
                    #     "transitions:\n"
                    #     "\"1cdA\"->\"ml8\"\n"
                    #     "\"ml8\"->\"\"\n"
                    #     "transitions end here\n"
                    #     "Answer:\n"
                    #     "\"solvable\": \"true\",\n"
                    #     "\"solution\": \"[0, 1, 1]\"\n"
                    # )

                    #3-shot
                    # prompt_text = (
                    #     "Here is a puzzle: \n"
                    #     "You start with an initial string and you are given a set of transitions. During a single transition, you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.\n"
                    #     "Solve this problem:\n"
                    #     f"initial string: {initial}\n"
                    #     "transitions:\n"
                    #     f"{transitions_str}"
                    #     "//transitions ends here\n"
                    #     "write a full solution with explanation of each step in the explanation field.\n"
                    #     "Explain if you think the problem is solvable by responding with \"yes or \"no in the solvable field.\n"
                    #     "The solution field should have an array of the indices of the rules you used in the solution (0 indexed from the top). Eg:[0,2,1](illustrative example)\n"
                    #     "Here are 3 examples:\n"
                    #     "initial string: 1cdAml8\n"
                    #     "transitions:\n"
                    #     "\"1cdA\"->\"ml8\"\n"
                    #     "\"ml8\"->\"\"\n"
                    #     "transitions end here\n"
                    #     "Answer:\n"
                    #     "\"solvable\": \"true\",\n"
                    #     "\"solution\": \"[0, 1, 1]\"\n"
                    #     "initial string: 3q3q\n"
                    #     "transitions:\n"
                    #     "\"3q\"->\"aR\"\n"
                    #     "\"aR\"->\"\"\n"
                    #     "transitions end here\n"
                    #     "Answer:\n"
                    #     "\"solvable\": \"true\",\n"
                    #     "\"solution\": \"[0, 0, 1, 1]\"\n"
                    #     "initial string: 0110110\n"
                    #     "transitions:\n"
                    #     "\"0\"->\"110110\"\n"
                    #     "\"110110\"->\"\"\n"
                    #     "transitions end here\n"
                    #     "Answer:\n"
                    #     "\"solvable\": \"true\",\n"
                    #     "\"solution\": \"[1,0,1,0,1]\"\n"
                    # )

                    #COT
                    prompt_text = (
                        "Here is a puzzle: \n"
                        "You start with an initial string and you are given a set of transitions. During a single transition, you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.\n"
                        "Solve this problem:\n"
                        f"initial string: {initial}\n"
                        "transitions:\n"
                        f"{transitions_str}"
                        "//transitions ends here\n"
                        "write a full solution with explanation of each step. however the last 2 lines should be in the below format.\n"
                        "if you are getting stuck, with no way to make the string blank, try retracing your steps to where you can choose a different transition to the one you chose before.\n"
                        "make sure you follow the solution format: the last 2 lines of the response should 1)solvable: \"yes\" or \"no\" and 2)solution:[0,2,1](example of a soln format) .Make sure both are separated by newlines and that there is no other text in the last 2 lines. the solution should be an array of the indices of the rules you used in the solution (0 indexed from the top)\n"
                        ""
                        "Here are 4 examples:\n"
                        "initial string: 1cdAml8\n"
                        "transitions:\n"
                        "\"1cdA\"->\"ml8\"\n"
                        "\"ml8\"->\"\"\n"
                        "transitions end here\n"
                        "Answer:\n"
                        "\"explanation\": \"We want to reduce the string to a blank string, so we want to use the transition that leads to blank string. We will use other transitions to convert other parts of the string to the part reducible to blank string. Transition 0 leads to ml8, which can then be reduced to blank string.\"\n"
                        "\"solvable\": \"true\",\n"
                        "\"solution\": \"[0, 1, 1]\"\n"
                        "initial string: 3q3q\n"
                        "transitions:\n"
                        "\"3q\"->\"aR\"\n"
                        "\"aR\"->\"\"\n"
                        "transitions end here\n"
                        "Answer:\n"
                        "\"explanation\": \"Like above,we want to use the transition that leads to blank string. We will use other transitions to convert other parts of the string to the part reducible to blank string. Transition 0 leads to aR, which can then be reduced to blank string. So we use this rule to convert to aR and then use given transition rules to get blank.\"\n"
                        "\"solvable\": \"true\",\n"
                        "\"solution\": \"[0, 0, 1, 1]\"\n"
                        "initial string: 01101100\n"
                        "transitions:\n"
                        "\"0\"->\"110110\"\n"
                        "\"110110\"->\"\"\n"
                        "transitions end here\n"
                        "Answer:\n"
                        "\"explanation\": \"In this case, we see that 0 cannot be directly reduced to blank, but by using transition 0 we get 110110 which can be directly reduced. Then we see 110110 which we can directly remove. The last 0 we can again remove by using rule 0 and then rule 1.\"\n"
                        "\"solvable\": \"true\",\n"
                        "\"solution\": \"[0,1,1,0,1]\"\n"
                        "initial string: 11001001\n"
                        "transitions:\n"
                        "\"1\"->\"0\"\n"
                        "\"1001\"->\"\"\n"
                        "transitions end here\n"
                        "Answer:\n"
                        "\"explanation\": \"First, let's try using transition 0 (step 1)to get 01001001. We then apply transition 1(step 2) to get 0001. From here we can apply transition 0(step 3) to get 0000. We cannot do anythingn from here.So, we retrace our steps. We see that at step 1 we could instead have used transition 1 to get 1001, and then at step 2 applied transition 1 again to get the required blank string in 2 steps.\"\n"
                        "\"solvable\": \"true\",\n"
                        "\"solution\": \"[1,1]\"\n"
                    )
                    prompts.append(prompt_text)
                    initial_strings.append(initial)
                    transitionList.append(transitions)
            except Exception as e:
                print("Error processing block:", e)
    return prompts,initial_strings,transitionList

#Json format validation function
# def validate(candidate_text, initial_string, transitions, id):
#     try:
#         result = json.loads(candidate_text)
#     except Exception as e:
#         print(f"Error parsing candidate_text for id {id}: {e}")
#         return False

#     solved = False
#     if result.get("solvable", "").lower() != "true" and result.get("solvable", "").lower() != "yes":
#         solved = False
#     else:
#         soln_str = result.get("solution", "")
#         # Clean up the solution string: remove brackets and trailing commas.
#         soln_str = soln_str.strip().lstrip("[").rstrip("]")
#         indices = [s.strip() for s in soln_str.split(",") if s.strip() != ""]
#         try:
#             indices = [int(s) for s in indices]
#         except Exception as e:
#             print(f"Error converting solution indices for id {id}: {e}")
#             solved = False
#         else:
#             current_str = initial_string
#             turns = 0
#             for idx in indices:
#                 if(current_str == ""):
#                     solved = False
#                     break
#                 if idx < 0 or idx >= len(transitions):
#                     solved = False
#                     break
#                 trans = transitions[idx]
#                 src = trans.get("src", "")
#                 tgt = trans.get("tgt", "")
#                 pos = current_str.find(src)
#                 if pos == -1:
#                     solved = False
#                     break
#                 current_str = current_str[:pos] + tgt + current_str[pos+len(src):]
#                 print(f"Current string: {current_str} after transition: {src}->{tgt}")
#                 turns += 1
#             if current_str == "" and turns == len(indices):
#                 solved = True
#             else:
#                 solved = False

#     result_obj = {
#         "id": f"\"{id}\"",
#         "solved": "true" if solved else "false",
#         "method": "z"
#     }
#     # CHANGED: Append the result to dataset_data.txt, with a comma and a blank line after each JSON object.
#     with open("dataset_data_3shot.txt", "a") as f:
#         f.write(json.dumps(result_obj, indent=4))
#         f.write(",\n\n")
#     print()
#     return solved

#Validate function for updated format
def validate(candidate_text, initial_string, transitions, id):
    """
    Validates candidate_text which is expected to be a JSON string produced
    from the PuzzleAnswer base model. The expected format is:

    {
      "explanation": <string>,
      "solvable": "yes" or "no",
      "solution": "[0, 1]"  (i.e. a string representing a list of indices)
    }
    
    The function parses the solution string, applies the transitions,
    and verifies that the final string is empty.
    """
    try:
        data = json.loads(candidate_text)
    except Exception as e:
        print(f"Error parsing candidate_text for id {id}: {e}")
        solved = False
    else:
        solvable_val = str(data.get("solvable", "")).strip().lower()
        if solvable_val not in ["yes", "true"]:
            solved = False
        else:
            soln = data.get("solution", "")
            # Expect solution to be a string like "[0, 1]"
            soln_str = soln.strip()
            if soln_str.startswith('"') and soln_str.endswith('"'):
                soln_str = soln_str[1:-1].strip()
            if not (soln_str.startswith("[") and soln_str.endswith("]")):
                solved = False
            else:
                inner = soln_str[1:-1].strip()
                if inner == "":
                    indices = []
                else:
                    indices = [s.strip() for s in inner.split(",") if s.strip() != ""]
                try:
                    indices = [int(x) for x in indices]
                except Exception as e:
                    print(f"Error converting solution indices for id {id}: {e}")
                    solved = False
                else:
                    current_str = initial_string
                    turns = 0
                    for idx in indices:
                        if current_str == "":
                            solved = False
                            break
                        if idx < 0 or idx >= len(transitions):
                            solved = False
                            break
                        trans = transitions[idx]
                        src = trans.get("src", "")
                        tgt = trans.get("tgt", "")
                        pos = current_str.find(src)
                        if pos == -1:
                            solved = False
                            break
                        current_str = current_str[:pos] + tgt + current_str[pos+len(src):]
                        print(f"Current string: {current_str} after transition: {src} -> {tgt}")
                        turns += 1
                    solved = (current_str == "" and turns == len(indices))
    
    result_obj = {
         "id": f"\"{id}\"",
         "solved": "true" if solved else "false",
         "method": "z"
    }
    with open("dataset_data_cotImproved.txt", "a") as f:
         f.write(json.dumps(result_obj, indent=4))
         f.write(",\n\n")
    return solved
    
def main():
    parser = argparse.ArgumentParser(description="Call Gemini API with provided API key.")
    parser.add_argument("--api_key", type=str, required=True, help="Your Gemini API key.")
    args = parser.parse_args()

    api_key = args.api_key
    id_start = int(input("Enter starting problem id: "))
    id_end = int(input("Enter ending problem id: "))
    
    temp_input = input("Enter temperature (default 1.0): ")
    temperature = float(temp_input) if temp_input.strip() else 1.0

    top_p_input = input("Enter top_p (default 1.0): ")
    top_p = float(top_p_input) if top_p_input.strip() else 1.0

    dataset_file = "dataset_middle.txt"  # CHANGED: Path to the dataset file.
    prompts,initial_strings,transitions = generate_prompts_from_dataset(dataset_file, id_start, id_end)

    # for transition in transitions:
    #     print(f"{transition[0]["src"]} and {transition[0]["tgt"]}")
    
    client = genai.Client(api_key = api_key)
    solutions = []
    
    no_prompts = 0
    for prompt in prompts:
        prompt = prompts[no_prompts]
        try:
            response_data = call_gemini_api(
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                client = client
            )
            try:
                candidate_text = response_data.candidates[0].content.parts[0].text
            except Exception as inner_e:
                print("Error parsing candidate_text, marking as unsolved.")
                candidate_text = '{"solvable": "false", "solution": []}'

            #format for new prompt string
            # try:
            #     candidate_text = response_data.candidates[0].content.parts[0].text
            # except Exception as inner_e:
            #     print("Error parsing candidate_text, marking as unsolved.")
            #     candidate_text = 'solvable: "false"\nsolution: []'
            solutions.append(candidate_text)
            # print(prompt)
            print(f"Problem {id_start+no_prompts} solved:")
            print(candidate_text)
            validate(candidate_text,initial_strings[no_prompts],transitions[no_prompts],id_start+no_prompts)
            no_prompts+=1
            if no_prompts % 15 == 14:
                print("Pausing for 1 minute to avoid rate limits...")
                time.sleep(60)

        except Exception as e:
            print("Error occurred:")
            print(e)
        

if __name__ == "__main__":
    main()