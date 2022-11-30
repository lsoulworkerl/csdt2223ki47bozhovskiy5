from database import input_db_data, check_db_data, get_db_data
from prettytable import PrettyTable

def main():
    i = int(input("What you want?\n1 - check data id db\n2 - run program\n"))

    if i == 1:
        result = get_db_data()
        
        #create table
        table = PrettyTable(['ID', 'input', 'output'])
        for i in result:
            table.add_row([i[0], i[1], i[2]])
        
        print(table)
        
    if i == 2:
        #get number 
        number = int(input("Please write your number 1-16\n"))

        #check this data in db
        result = check_db_data(number)

        #if we don't have this data
        if result == None:
            result = input_db_data(number)
        
        print("Your number is {0}, your result is {1}".format(number, result))


if __name__=="__main__":
    main()