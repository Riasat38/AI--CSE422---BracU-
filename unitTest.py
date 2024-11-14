from search import path_construct
import sys

def test_pathConstruct():
    parent = {
        "A" : "B",
        "C" : "D",
        "D" : "A",
        "F" : "C"
    }
    if path_construct(parent,"F") == ["B","A","D","C","F"] :
        print("OK")
    else:
        sys.exit("Error")

if __name__ == "__main__":
    test_pathConstruct()