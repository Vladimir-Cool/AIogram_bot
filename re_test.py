from re import match

NUM_DIGITS = 3

def num_valid(attempt):
    pre = "{" + str(NUM_DIGITS) + "}"
    pattern = r"\b\d{}\b".format(pre)
    print(pattern)

    if match(pattern, attempt):
        return True

    return False

print(match(r"\b[yYдД]", "тщ"))