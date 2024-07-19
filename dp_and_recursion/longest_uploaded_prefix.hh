#include <vector>

class LUPrefix {
public:
    LUPrefix(int n) {
        uploaded_ = std::vector<bool>(n+2, false);
        uploaded_[0] = true;
    }
    
    void upload(int video) {
        uploaded_[video] = true;
        if (video == lup_+1) {
            while (uploaded_[++lup_]);
            lup_--;
        }
    }
    
    int longest() {
        return lup_;
    }

private:
    int lup_ = 0;
    std::vector<bool> uploaded_;
};

/**
 * Your LUPrefix object will be instantiated and called as such:
 * LUPrefix* obj = new LUPrefix(n);
 * obj->upload(video);
 * int param_2 = obj->longest();
 */