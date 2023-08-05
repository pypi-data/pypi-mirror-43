from rememberme import memory, top

def test_top():
    a = [1, 2, 3]
    b = [1, 2]
    c = [1]
    res = top()
    assert [entry[0] for entry in res[:3]] == [a, b, c]

    class Node:
        def __init__(self, data):
            self.data = data

    n = Node(a)
    # the instance is the largest
    assert top(n)[0] == (n, memory(n))
    # the type is the second
    assert top(n)[1] == (Node, memory(Node))
    print("ok")


test_top()
