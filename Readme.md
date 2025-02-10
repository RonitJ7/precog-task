# Report
## Ronit Jalihal, 2023101028

## Brief Code Overview
### Dataset Generation:
+ This task is done using the dataset_gen.cpp program.
+ dataset_gen.cpp contains variables `MAX_LEN`, `MAX_RULES` and their corresponding minimum values to regulate difficulty of problems generated.
+ The general approach used for generating rules is randomisation. The number of rules, string length of both source and destination of each rule, the rule itself are all randomly generated.
+ Another rule is added with an empty destination.
+ Then, all the rules are reversed and strings are generated through DFS starting from a blank string.
+ This gaurantees that all random strings generated are solvable. Additionally it also gives the solution.
+ Data was curated from multiple runs of the program to get the final dataset.

### Testing through Gemini API:
+ Gemini API is used to test the datasets using various differnet prompting techniques and parameter values.
+ The `validate` function is used to check whether answer provided by the LLM is correct or not.

### Jsonify.py:
+ Used to convert the dataset from text format in `dataset_middle.txt` to unique json files for each problem and solution in the dataset.

## Dataset Selection:
### Selecting appropriate difficulties
+ Difficulty was adjusted 

## Prompt Selection:
### Zero Shot prompts:
- Prompt used for testing on web interfaces was (with a sample example):   <br>
    Here is a puzzle: <br>
    You start with an initial string and you are given a set of transitions. During a single transition,you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.<br>
    Solve this problem:<br>
    initial string: 001110000101100<br>
    transitions:<br>
    "010110"->"111011"<br>
    "001110"->""<br>
    "11101"->"11"<br>
    "000"->"10111"<br>

- Prompt used during Gemini API was (in python string format):<br>
 "Here is a puzzle: \n"<br>
"You start with an initial string and you are given a set of transitions. During a single transition, you can only apply the rule on the first instance of the substring in the string. Your goal is to get the empty string.\n"<br>
"Solve this problem:\n"<br>
f"initial string: {initial}\n"<br>
"transitions:\n"<br>
f"{transitions_str}"<br>
"//transitions ends here\n"<br>
"report the answer in given json format. the solution should be an array of the indices of the rules you used in the solution (0 indexed from the top)"<br>