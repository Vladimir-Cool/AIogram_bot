
def repeat_num(str_to_check):
    check_dict = dict()
    for i in range(10):
        check_dict[i] = 0
    for num in str_to_check:
        check_dict[int(num)] += 1
        if check_dict[int(num)] > 1:
            return False
    return True

print(repeat_num("890"))