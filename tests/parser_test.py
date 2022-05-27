from cgitb import reset
import re

TXT = 1
SUB = 2
CIT = 3

def parse(text):

    # Search if the input is subscribtion change
    subscribtion = re.findall(r'\$\d+', text)
    if subscribtion:
        return SUB, int(subscribtion[0][1:])
    
    # Search for a citation in text
    citation = re.findall(r'%\d+%', text)
    if citation:
        return CIT, int(citation[0][1:-1])

    # Otherwise no special substring present
    return TXT, text


def parser_test():

    text = parse("Hello world!")
    assert text[0] == TXT
    assert text[1] == "Hello world!"
    print(text)

    sub = parse("$2137")
    assert sub[0] == SUB
    assert sub[1] == 2137
    print(sub)

    result = parse("$")
    print(result)

    cit = parse("And as %42% was saying")
    assert cit[0] == CIT
    assert cit[1] == 42
    print(cit)

    empty = parse("")

    print(empty)
    assert empty[0] == TXT
    assert empty[1] == ""
    assert not empty[1]
    print("All Tests Passed!")


if __name__ == "__main__":
    parser_test()
