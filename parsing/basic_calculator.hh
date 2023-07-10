#pragma once

#include <set>
#include <string>
#include <vector>

/**
 * Solution to https://leetcode.com/problems/basic-calculator/ 
 */  

struct Token {
    bool is_number;
    int value;
    std::string symbol;  // one of +, -, (, and )
    
    Token() = default;
    
    Token(int value) : is_number(true), value(value) {}

    Token(bool is_number, std::string str) {
        this->is_number = is_number;
        value = is_number ? stoi(str) : 0;
        symbol = is_number ? "" : str;
    }
    
    bool is_plus() {
        return symbol == "+";
    }

    bool is_minus() {
        return symbol == "-";
    }

    bool is_paren() {
        return is_open() || is_close();
    }

    bool is_open() {
        return symbol == "(";
    }

    bool is_close() {
        return symbol == ")";
    }
};  // struct Token

class BasicCalculator {
public:
    int calculate(std::string s) {
        symbols_ = std::set<std::string>{"+", "-", "(", ")"};
        std::vector<Token> tokens = tokenize(s);
        StackParser parser;
        for (auto& token : tokens) {
            parser.push(token);
        }
        return parser.flush();
    }
    
private:
    /**
     * Tokenizes a given string.
     */
    std::vector<Token> tokenize(std::string s) {
        std::vector<Token> result;
        std::string curr_num = "";
        for (int i = 0; i < s.size(); ++i) {
            std::string curr_char = s.substr(i, 1);
            if (curr_char == " ") continue;
            if (symbols_.count(curr_char)) {
                // One of +, -, (, or )
                if (curr_num.size()) {
                    // complete the construction of the current number
                    result.emplace_back(true, curr_num);
                    curr_num = "";
                }
                result.emplace_back(false, curr_char);
            } else {
                // digit
                curr_num += curr_char;
            }
        }
        // end of loop, check for constructed number
        if (curr_num.size()) result.emplace_back(true, curr_num);
        return result;
    }
    
    class StackParser {
    public:
        void push(Token& token) {
            if (!token.is_paren()) {
                 // Not a paren - simply push token onto stack
                return stack_.push_back(token);
            }
            
            if (token.is_open()) {
                // Note location of the newest open paren
                stack_.push_back(token);
                open_parens_.push_back(stack_.size() - 1);
                return;
            } else {
                pop_last_open();
            }
            
        }
        
        /**
         * \pre all open brackets must have been matched by closing 
         *      brackets
         */
        int flush() {
            return evaluate(0);
        }
        
    private:
        /**
         * Replaces the expression following the last open parenthesis with its evaluation.
         */
        void pop_last_open() {
            int last_open_idx = open_parens_.back();
            open_parens_.pop_back();
            int partial = evaluate(last_open_idx+1);
            stack_.resize(last_open_idx);
            stack_.emplace_back(partial);
        }
        
        /**
         * Evaluates expression starting at start_idx, ending 
         * at end of the stack_ .
         * \pre the section of stack_ being evaluated must contain
         * no parentheses.
         */
        int evaluate(int start_idx) {
            int value = 0;
            int multiplier = 1;
            
            for (int i = start_idx; i < stack_.size(); ++i) {
                Token token = stack_[i];
                if (token.is_number) {
                    value += multiplier * token.value;
                } else {
                    multiplier = token.is_plus() ? 1 : -1;
                }
            }
            return value;
        }
        
        // Data members
        
        /**
         * Current, partially processed list of tokens
         * Invariants:
         * (i) Never contains a closing brace
         */
        std::vector<Token> stack_;  
        
        // indices of open parentheses
        std::vector<int> open_parens_;  
        
    };  // class StackParser
    
    // Data members
    std::set<std::string> symbols_;
};
