class Solution {
public:
    vector<string> fullJustify(vector<string>& words, int maxWidth) {
        width_ = maxWidth;
        vector<vector<string>> lines = splitLines(words);
        vector<string> result;
        for (auto& line : lines) {
            result.emplace_back(justify(line));
        }
    }

private:
    vector<vector<string>> splitLines(vector<string>& words) {
        vector<vector<string>> lines;
        int spaceLeft = width_;
        vector<string> currLine;
        for (auto& word : words) {
            if (word.size() <= spaceLeft) {
                // Add word to the current line
                currLine.push_back(word);
                spaceLeft -= (word.size() + 1);
            } else {
                // flush currLine and start a new line
                lines.push_back(currLine);
                currLine = vector<string>();
                spaceLeft = width_;
            }
        }
        // handle unflushed last line
        if (currLine.size()) {
            lines.push_back(currLine);
        }
        return lines;
    }
    
    string justify(vector<string>& line) {
        // Suppose we have k words w0, w1, ..., w_{k-1}
        // Handle k = 1 case separately, assume k >= 2 for now
        // Final str is w0a0w1a1...a_{k-2}w_{k-1}
        // Need to calculate values a0, ..., a_{k-2}
        // Their sum Sa = width_ - Sw
        // Let Sa = (k-1) * q + r
        // ai = q + (i <= r-1)
        // TODO - implement
    } 

    int width_;
};
