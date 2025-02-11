# Project Desciption
### Report.md is pushed onto github.
### Video link (just slides): 
https://drive.google.com/file/d/1LcFS7ZDkDfDV5FhHEpd50GA4ZoMYMji0/view
### Video link (with voiceover): https://www.loom.com/share/31548eb706704d1e88c60828bd63d4a5
## Directory Structure
### problems and solutions directories
+ problems directory contains 100 json files, one for each problem in the dataset. It outlines each problem in the dataset in json format.
+ solutions directory is similar to problems directory, with one json file for each problem. It provides solutions to each problem.

### results
#### json_format:
+ This contains the 3 files for results of zero shot, 1 shot and 3 shot testing done with the json output format without explanation.
#### text format:
##### base:
This contains the 4 files for results of zero, 1 ,3 shot as well as COT prompting.
#### temp-0.7:
This contains the results of COT prompting for temperature 0.7
#### temp-0.85:
This contains the result data of COT prompts with the default 1 value of top_p. 
##### top_p-0.85
This contains the result data of COT prompts with value of top_p = 0.85
##### top_p-0.95
This contains the result data of COT prompts with value of top_p = 0.95

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

### dataset_middle.txt
+ Used as a convenient way to store problems to make it easy to access for Gemini API file.

## Commands to run project:
+ jsonify.py:<br> ` python3 jsonify.py `
+ geminiApi.py:<br>
 `python3 geminiApi.py --api_key [Insert API KEY here]`
 + dataset_gen.cpp:<br>
`g++ dataset_gen.cpp `


## Main libraries:
+ jsonify.py:  os, json
+ geminiApi.py: google-genai, pydantic , json ,argparse, time