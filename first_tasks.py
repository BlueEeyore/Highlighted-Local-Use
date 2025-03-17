def hello_world():
    print("Hello World!")

def greeting():
    name = input("What's your name?\n")
    #print(f"Hello {name}")
    print("Hello " + name)

def clean_int(string):
    nums = [str(x) for x in range(10)] + ["-", "+", "."]
    is_float = False
    for i, x in enumerate(string):
        if x == ".":
            if is_float:
                return string
            else:
                is_float = True
        if x == "-" and i != 0:
            return string
        if x not in nums:
            return string
    if is_float:
        return float(string)
    return int(string)

def calc():
    all_ints = False
    while not all_ints:
        a, b = clean_int(input("first number?\n")), clean_int(input("second number?\n"))
        if type(a) != str and type(b) != str:
            all_ints = True
        else:
            print("Try again")
    result = round(a + b, 7)
    if str(result)[-2:] == ".0":
        result = int(result)
    print(result)

calc()
