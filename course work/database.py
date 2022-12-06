import psycopg2
from config import host, user, password, db_name


def get_record():
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
                """SELECT nickname, score FROM record ORDER BY score"""
            )
            result = cursor.fetchall()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        #end of word with db
        if connection:
            connection.close()

    return result


def input_record(nickname, score):
    try:
        #login in db
        connection = psycopg2.connect(
            host = host,
            user = user,
            password = password,
            database = db_name,
        )
        connection.autocommit = True

        #add new data to db
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO record (nickname, score) VALUES ('{0}', {1})""".
                format(str(nickname), str(score))
            )

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        #end of word with db
        if connection:
            connection.close()

def main():
    result = get_record()
    result.reverse()
    print(result[0:10])


if __name__ == "__main__":
    main()