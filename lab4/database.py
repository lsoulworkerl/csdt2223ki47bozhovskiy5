import psycopg2
from config import host, user, password, db_name
from parser import parser


def get_db_data():
    try:
        #login in db
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT * FROM data"""
            )
            result = cursor.fetchall()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        #end of word with db
        if connection:
            connection.close()

    return result


def input_db_data(input):
    try:
        #login in db
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
        )
        connection.autocommit = True

        #run parser
        result = parser(str(input))

        #add new data to db
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO data (input, output) VALUES ({0}, {1})"""
                .format(input, result)
            )

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        #end of word with db
        if connection:
            connection.close()

    return result


def check_db_data(input):
    try:
        #login in db
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT output FROM data WHERE input = {0}""".format(input)
            )
            result = cursor.fetchone()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        #end of word with db
        if connection:
            connection.close()
            
    #check None
    if result == None:
        return result

    return result[0]


def main():
    input_db_data(3)


if __name__=="__main__":
    main()