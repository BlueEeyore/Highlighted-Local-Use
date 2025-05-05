class LogicalStack:
    def __init__(self):
        self.stack = []

    def push(self, message):
        """adds message on to the end of the LogicalStack"""
        self.stack.append(message)

    def pop(self):
        """removes and returns final item of the LogicalStack"""
        result = self.stack.pop()
        return result

    def dump(self):
        """returns each item of the stack on individual lines"""
        return "\n -".join(self.stack)

if __name__ == "__main__":
    # test
    trace = LogicalStack()
    trace.push("Initialize system")
    trace.push("Load config")
    trace.push("Connect to DB")

    print(trace.dump())
