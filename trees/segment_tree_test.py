from segment_tree import SegmentTree 

def test_basic():
    data = [1, 4, 7, 11, 20]
    stree = SegmentTree(data, lambda x, y: x+y)
    psum = stree.query(0, 3)  # sum of inclusive range [0, 3]
    assert psum == 23, f"expected 23 but got {psum}"
    stree.update(0, 5)
    stree.update(2, 6) # data is now [5, 4, 6, 11, 20]
    psum = stree.query(0, 3)
    assert psum == 26, f"Expected 26 but got {psum}"
    stree.update(2, 7)
    stree.update(4, 30) # data is now [5, 4, 7, 11, 30]
    psum = stree.query(3, 4)
    assert psum == 41, f"Expected 41 but got {psum}"
    psum = stree.query(0, 4)
    assert psum == 57, f"Expected 57 but got {psum}"
    print("Success")

if __name__=="__main__":
    test_basic()