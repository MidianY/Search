
class Query:

    if __name__ == "__main__":
        while True:
            inputs = input("Enter an input: ")
            if inputs == ":quit":
                break
            print(inputs.upper())
            print(inputs.getQuery().upper())