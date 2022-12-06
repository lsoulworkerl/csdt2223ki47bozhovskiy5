from database import *


def test_database():
    input_record('test', 10)
    print("Put test and 10")
    result = get_record()
    for i in result:
        if i == ('test', 10):
            print("Get test and 10")
            return 1
    print("Can't get")
    return 0 


def check_output_database():
    result = get_record()
    if result != None:
        print("DB work")
        return 1
    if result == None:
        print("DB don't work")
        return 0 


def check_nickname(nickname):
    if nickname != None and nickname != "":
        print("Test completed GOOD")
    if nickname == "":
        print("NICKNAME DON'T GET")
    else:
        print("NICKNAME DON'T GET")


if __name__=="__main__":
    good_test = 0
    sum_test = 2
    test_1 = test_database()
    test_2 = check_output_database()
    good_test += test_1
    good_test += test_2 
    print("{0} out of {1} completed successfully".format(good_test, sum_test))