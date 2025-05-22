from error import ErrorStack

error_stack = ErrorStack()

def openfile(fn):
    """opens file with filename fn"""
    try:
        f = open(fn)
    except Exception as e:
        error_stack.push(str(e))
        return None
    return True

def processfile(fn):
    """processes file with filename fn"""
    print(f"trying to process {fn}")
    result = openfile(fn)
    if result is None:
        error_stack.push(f"failed to open file {fn}")
        return None
    return True

def main():
    """main func"""
    result = processfile("arsietnairseotn")
    if result is None:
        print(error_stack.dump())

main()
