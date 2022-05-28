

def foo():
    i = 0
    while True:
        print("In foo()")
        yield i
        i += 1

def main():
    a = 1
    for i in foo():
        print("in main()")
        for _ in range(10000000):
            a += 1
        print(i)

if __name__ == "__main__":
    main()