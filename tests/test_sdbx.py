

def foo():
    for i in range(5):
        print("In foo()")
        yield i

def main():
    for i in foo():
        print("in main()")
        print(i)

if __name__ == "__main__":
    main()