# Report
## Ronit Jalihal, Roll No: 2023101028
## Theme: Math and AI

## Tasks done
### Task 1
I have done this my best to create a dataset with varying difficulty suitable for AI and as close to representing puzzles on the sed-game website as possible with random transitions and starting string. The dataset is of size 100.

### Task 2
I started off with using the web interfaces and eventually moved on to Gemini API using Flash 2.0. I experimented with using zero shot, 1shot, 3shot and COT prompting, as well as changing values of temperature and top_p for better results.

### Task 3
Not satisfactorily completed.<br>
I was unable to find a metric that could compare two unsuccessful responses and assign a number to each.<br>
### Task 4
Examples of both cases are provided

## Dataset Selection:
### Selecting appropriate difficulties
+ Difficulty was adjusted by setting the value of the following variables:
1. `MAX_RULES` and `MAX_LEN`: Decreasing  leads to lower difficulty and vice versa.
2. `MIN_RULES` and `MIN_LEN`: Increasing leads to higher difficulty and vice versa

+ After a little trial and error, it was clear that a problem given in binary alphabet would likely be more difficult. This is because at each step there are more number of possible rules to take making it harder to efficiently solve the problem for both humans and AI.

+ Similarly, selecting input alphabet to both numbers and lower case alphabet, or number and was more likely to create a difficult puzzle. This effect is not as stark as that of the bianry though.

### Number of problems in each difficulty level
AI was unable to reliably find and use patterns that humans would find, despite my best efforts using COT and 3-shot prompting.
+ Problems from 1-20 are very easy for humans.
+ Problems from 21-51 are easy. 
+ Problems 52-60 are a slight jump in difficulty compared to 21-51.
+ Problems 61-74 have a significant spike compared to earlier problems. A human can still solve them within 3 minutes. 
+ Problems 75-100 are difficult, even for humans.

Best Accuracies obtained for each of these sections:<br>
+ 12/20 for problems from 1-20
+ 16/31 for problems from 21-51
+ 5/9 for problems from 52-60
+ 6/14 for problems from 61-74
+ 0/26 for problems from 75-100

### Selecting input alphabets:
+ A wide range of input alphabets are used: numbers, lowercase letters, uppercase letters, binary as well as special characters like . , o , [ , ] and _ 
+ This was done to better represent the variety of input alphabets on the sed puzzle website, and also to make the game harder.
+ Additionally, there are multiple puzzles where numbers, lowercase letters and uppercase letters are all combined with each other. 
## Prompt Selection:
### Zero Shot:
This was a simple prompt that described the rules and goal of the game and gave it the puzzle. It closed by describing the output format.

### One shot:
This prompt was the same as the one for zero shot but with an example added on. I chose the below problem as an example: <br>
```
#     initial string: 1cdAml8
#     transitions:
#     1cdA->ml8
#     ml8-> " "
#     Answer:
#     solvable : true
#     solution : [0, 1, 1]
```
I chose this problem as it demonstrated a logical method to solve the easier questions, which I noticed Gemini was struggling with. There was a marked improvement due to this in performance of easier questions.

### Three shot:
The first example was the same as one shot. <br>
The second example was: <br>
```
#     initial string: 3q3q
#     transitions:
#     3q->aR
#     aR-> ""
#     Answer:
#     solvable: true
#     solution: [0, 0, 1, 1]
```
I chose this problem since it was basically the first problem with one additional step. I did this so that some of the easier questions which were still not solved would be solved with the help of this guideline.<br>
The third example was: <br>
```
#     initial string: 0110110
#     transitions:
#     0->110110
#     110110-> ""
#     Answer:
#     solvable: true,
#     solution: [1,0,1,0,1]
```
I chose this problem as a problem harder than the two ones before so that the model would be able to solve some of the easier questions in the 20-61 range.

### COT:
The first three examples were again the same.<br>
Their explanations were basically to guide the model to use transitions in such a way to get substrings that lead to blank string if possible.<br>
The fourth example was:<br>
```
#     initial string: 11001001
#     transitions:
#     1->0
#     1001-> ""
#     Answer:
#     solvable: true,
#     solution: [1,1]
```

This was to introduce the model to backtracking, where a certain line would lead to failure, so you could backtrack and recheck for alternative paths in the tree.<br>
The explanation given reflects this backtracing concept.

## Methodology and results:
### JSON Outputs
+ I began using the gemini API, taking output from it in the JSON format:<br>
```
class PuzzleAnswer(BaseModel):
    solvable: str
    solution: str
```
+ I tested zero shot, 1 shot and 3 shot prompting with the following results:<br>
<table>
  <thead>
    <tr>
      <th></th>
      <th>Zero shot</th>
      <th>1 shot</th>
      <th>3 shot</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Accuracy</td>
      <td>17%</td>
      <td>19%</td>
      <td>22%</td>
    </tr>
  </tbody>
</table>

+ I soon realised that my prompts on the web interface were giving me much better results. I realised that the model performs better if you ask it to give it an explanation. So I changed the JSON outputs to the below format:<br>
```
class PuzzleAnswer(BaseModel):
    explanation: str
    solvable: str
    solution: str
```

### Text outputs
+ I instantly saw better results with this methodoloy. The results of this are outlined below:<br>
<table>
  <thead>
    <tr>
      <th></th>
      <th>Zero shot</th>
      <th>1 shot</th>
      <th>3 shot</th>
      <th>COT</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Accuracy</td>
      <td>29%</td>
      <td>34%</td>
      <td>36%</td>
      <td>36%</td>
    </tr>
  </tbody>
</table>

+ I next started experimenting with temperature and top_p values passed to the model. 
1. Temperature(0-2): Controls randomness in text generation.
A higher temperature (e.g., 1.0 or above) makes the output more random and creative, increasing variability and vice versa for lower temperatures.
2. Top_p(0-1): Instead of choosing from all possible words, top_p restricts choices to the top percentage of most likely words.Lower top_p makes responses more focused and predictable, while higher top_p allows more varied and creative responses.

+ The default values for both of these were 1.

+ Since solving sed-puzzle is a logical task, I decided to try decreasing temperature and top_p to see if it decreases hallucinations or improves transition-finding consistency.

+ The output for these using COT prompting (as it performed best) is shown for different values of temperature (with default top_p):

<table>
  <thead>
    <tr>
      <th></th>
      <th>0.7</th>
      <th>0.85</th>

  </thead>
  <tbody>
    <tr>
      <td>Accuracy</td>
      <td>33%</td>
      <td>38%</td>
    </tr>
  </tbody>
</table>


+ Using temperature 0.85, the accuracy increased to 38%.

+ Using top_p for various values, I got the following results:

<table>
  <thead>
    <tr>
      <th></th>
      <th>0.85</th>
      <th>0.95</th>

  </thead>
  <tbody>
    <tr>
      <td>Accuracy</td>
      <td>33%</td>
      <td>34%</td>
    </tr>
  </tbody>
</table>

+ Accuracy values decreased when reducing top_p, so I kept it at 1.

+ So I got my best result with the COT prompting technique, using temperature = 0.85 and top_p = 1.

## Metrics used:
### Accuracy
 This was the most basic metric used. It basically measured the number of correct responses over total responses. A high accuracy meant that the model was more likely to give a correct response.

### Deny%
A potential second metric to use is the percentage of responses where the LLM returns "no" to the solvable field, signifying lack of analytic capability,

### Length of final string:
Length of final string highlights to what extent the LLM succeeded in reducing initial string.

## Man Vs Machine:
### Problems easy for humans but difficult for AI:
 There were numerous problems that humans could do quite easily but Gemini couldn't solve despite my best efforts:<br>
Problem no.5: <br>
```
{
  "problem_id": "5",
  "initial_string": "001001111",
  "transitions": [
    {
      "src": "1",
      "tgt": "00100"
    },
    {
      "src": "1000001000",
      "tgt": "000"
    },
    {
      "src": "00100",
      "tgt": ""
    }
  ]
}
```
Humans can easily see the pattern of using transition 0 to convert "1" to "00100" and then using transition 2 to get the blank string. However, it is difficult for AI to visualise these patterns and choose the required transition out of all the possible transitions.<br>
Two other examples demonstrating this lack of pattern recognition are:<br>
Problem 11:<br>
```
{
  "problem_id": "11",
  "initial_string": "ITILITIT",
  "transitions": [
    {
      "src": "T",
      "tgt": "L"
    },
    {
      "src": "IL",
      "tgt": ""
    }
  ]
}
```

Problem 20: <br>
```
{
  "problem_id": "20",
  "initial_string": "WQGAU",
  "transitions": [
    {
      "src": "Sa",
      "tgt": "HSO"
    },
    {
      "src": "G",
      "tgt": "A"
    },
    {
      "src": "A",
      "tgt": "H"
    },
    {
      "src": "WQAHU",
      "tgt": ""
    }
  ],
"solution": "[2,1,3,]"
}
```

Both of these problems are very easy for humans, but AI was not able to solve them.

### Difficult problems solved by AI:
While all problems solved by AI could also feasibly be done by humans, there are some that are difficult for humans to solve and for which AI took less time compared to humans:

Problem 73:
```
{
  "problem_id": "73",
  "initial_string": "jd7FgKmC1GIajd7FD1GIa",
  "transitions": [
    {
      "src": "gKmC",
      "tgt": "D"
    },
    {
      "src": "7Fw1",
      "tgt": "Q"
    },
    {
      "src": "D",
      "tgt": "w"
    },
    {
      "src": "KC",
      "tgt": "u9c"
    },
    {
      "src": "jdQGIa",
      "tgt": ""
    }
  ],
}
```
Solution of this problem: [0,2,2,1,1,4,4] <br>
This problem involves random strings as well as comparatively less logical sense, so it takes longer for humans to solve.<br>

Similar are the two problems:<br>
problem 65:
```
{
  "problem_id": "65",
  "initial_string": "UMLTMEDQUMLTMEDJMH",
  "transitions": [
    {
      "src": "MAD",
      "tgt": "K"
    },
    {
      "src": "FXSKHN",
      "tgt": "OJBJYLJ"
    },
    {
      "src": "LTME",
      "tgt": "A"
    },
    {
      "src": "KQAUS",
      "tgt": "C"
    },
    {
      "src": "JMH",
      "tgt": "Q"
    },
    {
      "src": "UKQ",
      "tgt": ""
    }
  ],
}
```
Solution of this problem: [2,0,5,4,2,0,5]<br>

problem 64:
```
{
  "problem_id": "64",
  "initial_string": "HTVQWBQHTWBDEDBQ",
  "transitions": [
    {
      "src": "NBDED",
      "tgt": "Z"
    },
    {
      "src": "KCUQ",
      "tgt": "SQWFRC"
    },
    {
      "src": "W",
      "tgt": "N"
    },
    {
      "src": "CA",
      "tgt": "HFIKDGF"
    },
    {
      "src": "VQW",
      "tgt": "Z"
    },
    {
      "src": "HTZBQ",
      "tgt": ""
    }
  ],
}
```
solution of this problem : [4,5,2,1,5]

## Conclusion:
During this activity, I :
+ Made a dataset generation program and used it to curate a suitable dataset.
+ Used prompt engineering techniques to get better results.
+ Tuned the parameters used for best success chance.
+ Analysed the results obtained.