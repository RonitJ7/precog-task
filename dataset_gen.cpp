#include <bits/stdc++.h>
#include <fstream>
using namespace std;
#define MAX_LEN 15
#define MAX_RULES 10
#define MIN_LEN 1
#define MIN_RULES 2

void printString(string &curr, vector<int> &ruleSequence, ofstream &file)
{
    if (curr.size() >= MIN_LEN && ruleSequence.size() >= MIN_RULES)
    {
        file << curr << '\n';
        for (auto x : ruleSequence)
            file << x;
        file << "\n\n";
    }
}

void generate(vector<pair<string,string> > mp, vector<int> ruleSequence, string curr,ofstream &file)
{
    // cout << "Current string: " << curr << '\n';
    // cout << "Current rules: ";
    // cout << "\n\n";
    if (curr.size() >= MAX_LEN || ruleSequence.size() >= MAX_RULES)
    {
        return;
    }
    int numRules = mp.size();
    int currRule = 0;
    string currCopy = curr;
    for (auto check : mp)
    {
        cout<<"Current rule: "<<currRule<<' '<<"and length of sequence: "<<ruleSequence.size()<<'\n';
        if (check.first.size() == 0)
        {
            curr.insert(0, check.second);
            ruleSequence.push_back(currRule);
            printString(curr, ruleSequence,file);
            generate(mp, ruleSequence, curr,file);
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
                else
                {
                    curr_match = 0;
                }
                if (curr_match == curr_rule_len)
                {
                    int begin_substring = i - curr_rule_len + 1;
                    curr.erase(begin_substring, curr_rule_len);
                    curr.insert(begin_substring, check.second);
                    ruleSequence.push_back(currRule);
                    printString(curr, ruleSequence,file);
                    generate(mp, ruleSequence, curr,file);
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
    vector<string> rules = {"","helloworld","h","","e","","l","","o",""};
    // cout<<"Size of rules: "<<rules.size()<<'\n';
    vector<pair<string,string>> reversedRules;
    for (int i = 0; i < rules.size(); i += 2)
    {
        reversedRules.push_back({rules[i], rules[i + 1]});
    }
    int max_len = MAX_LEN;
    int max_rules = MAX_RULES;
    vector<int> ruleSequence;
    ofstream file;
    file.open("results.txt");
    // file.open("results.txt",fstream::app);
    file << reversedRules.size() << '\n';
    for (auto rules : reversedRules)
    {
        file << '"' << rules.second << '"' << " " << '"' << rules.first << '"' << '\n';
    }
    file <<'\n';
    generate(reversedRules, ruleSequence, "",file);
}