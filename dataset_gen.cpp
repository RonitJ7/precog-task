#include <bits/stdc++.h>
#include <fstream>
using namespace std;
#define MAX_LEN 60
#define MAX_RULES 20
#define MIN_LEN 20
#define MIN_RULES 15
#define MAX_RULES_NULL 12
#define MIN_UNIQUE_VALUES 4
#define MAX_CURR_RULE_PRINTS 8

int current = 1;
int current_rules_prints = 0;
string generateRandomString(int maxLength)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(0,1); // Generates numbers between 0 and 61 (inclusive)
    uniform_int_distribution<> distribLen(1, maxLength);

    int length = distribLen(gen); // Random length between 0 and maxLength
    string randomString = "";
    for (int i = 0; i < length; ++i)
    {
        int randVal = distrib(gen);
        char nextChar;

        if (randVal < 10)
        {
            // vector<char> brackets = {'[',']','_'};
            // nextChar = brackets[randVal];
            nextChar = '0' + randVal; // 0-9
        }
        else if (randVal < 36)
        {
            nextChar = 'A' + (randVal - 10); // A-Z
        }
        else
        {
            nextChar = 'a' + (randVal - 36); // a-z
        }
        randomString += nextChar;
    }
    return randomString;
}

vector<string> generateRandomRules(int maxRules, int maxRuleLength)
{
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<> distrib(2, maxRules); // At least one rule

    int numRules = distrib(gen);
    vector<string> rules(2*numRules);

    // Generate all rules with random strings.
    for (int i = 0; i < 2*numRules; ++i)
    {
        rules[i] = generateRandomString(maxRuleLength);
    }

    // Create a new rules vector that begins with an extra rule
    // whose src is an empty string and whose destination is null (empty string).
    vector<string> newRules;
    newRules.push_back(generateRandomString(MAX_RULES_NULL));  // Extra rule's src is a larger random string.
    newRules.push_back("");  // Extra rule's destination is null.

    // Append the previously generated rules.
    newRules.insert(newRules.end(), rules.begin(), rules.end());
    return newRules;
}

void printString(string &curr, vector<int> &ruleSequence, ofstream &file, vector<pair<string, string>> mp)
{
    if(current > 100 || ruleSequence.size() == 0){
        exit(0);
    }
    unordered_set<int> uniqueValues(ruleSequence.begin(), ruleSequence.end());

    if (curr.size() >= MIN_LEN && ruleSequence.size() >= MIN_RULES && uniqueValues.size() >= MIN_UNIQUE_VALUES && current_rules_prints <= MAX_CURR_RULE_PRINTS)
    {
        cout<<"Writing current: "<<current<<'\n';
        file << "{\n";
        file << "  \"problem_id\": \"" << current << "\",\n";
        file << "  \"initial_string\": \"" << curr << "\",\n";
        file << "  \"transitions\": [\n";
        for (size_t i = 0; i < mp.size(); i++)
        {
            file << "    {\n";
            file << "      \"src\": \"" << mp[i].second << "\",\n";
            file << "      \"tgt\": \"" << mp[i].first << "\"\n";
            file << "    }";
            if (i < mp.size() - 1)
                file << ",";
            file << "\n";
        }
        file << "  ],\n";
        file <<"\"solution\": ";
        file <<"\"[";
        int len = ruleSequence.size();
        for(int i = len-1;i>=0;i--){
            file << ruleSequence[i]<< ",";
        }
        file<<"]\"\n";
        file << "}\n\n";
        current++;
        current_rules_prints++;
    }
}

void generate(vector<pair<string, string>> mp, vector<int> ruleSequence, string curr, ofstream &file)
{
    if (curr.size() >= MAX_LEN || ruleSequence.size() >= MAX_RULES)
    {
        return;
    }
    int numRules = mp.size();
    int currRule = 0;
    string currCopy = curr;
    for (auto check : mp)
    {
        if (check.first.size() == 0)
        {
            curr.insert(0, check.second);
            ruleSequence.push_back(currRule);
            printString(curr, ruleSequence, file, mp);
            generate(mp, ruleSequence, curr, file);
            ruleSequence.pop_back();
        }
        else
        {
            int len = curr.size();
            int curr_match = 0;
            int curr_rule_len = check.first.size();
            for (int i = 0; i < len; i++)
            {
                if (curr[i] == check.first[curr_match])
                {
                    curr_match++;
                }
                else if (curr[i] != check.first[0])
                {
                    curr_match = 0;
                }
                else
                {
                    curr_match = 1;
                }
                if (curr_match == curr_rule_len)
                {
                    int begin_substring = i - curr_rule_len + 1;
                    curr.erase(begin_substring, curr_rule_len);
                    curr.insert(begin_substring, check.second);
                    ruleSequence.push_back(currRule);
                    printString(curr, ruleSequence, file, mp);
                    generate(mp, ruleSequence, curr, file);
                    ruleSequence.pop_back();
                    break;
                }
            }
        }
        curr = currCopy;
        currRule++;
    }
}
signed main()
{
    int maxRules = 8;      // Maximum number of rules
    int maxRuleLength = 12; // Maximum length of each rule


    ofstream file;
    file.open("results.txt");
    // file.open("results.txt",fstream::app);
    while(current <= 100){
        current_rules_prints = 0;
        vector<string> rules = generateRandomRules(maxRules, maxRuleLength);
        reverse(rules.begin(), rules.end());
        vector<pair<string, string>> reversedRules;
        for (int i = 0; i < rules.size(); i += 2)
        {
            reversedRules.push_back({rules[i], rules[i + 1]});
        }
        int max_len = MAX_LEN;
        int max_rules = MAX_RULES;
        vector<int> ruleSequence;
        generate(reversedRules, ruleSequence, "", file);
    }
    file.close();
}