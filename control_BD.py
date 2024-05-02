import psycopg2

class MyBD():
    def __init__(self, host='localhost', port=5432, user='user', password='mypassword', dbname='mydb'):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.dbname = dbname
        self.connect_myBD()

    def connect_myBD(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname,
                )
            print("Connection successful ...")
        except psycopg2.Error as e:
            print("Connection error:", e)

    def connect_close(self):
        self.connection.close()

    def get_password_for_login(self, login):
        try:
            with self.connection.cursor() as cursor:
                self.insert_query = "SELECT password " \
                                    "FROM interviewer " \
                                    "WHERE login = (%s);"

                cursor.execute(self.insert_query, (login,))
                password = cursor.fetchone()[0]

        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return False

        else:
            self.connect_close()
            print("Successfully inserted")
            print("Connection closed ...")
            print(password)
            return password
    def get_interviewer_all(self):
        self.connect_myBD()
        try:
            with self.connection.cursor() as cursor:

                self.insert_query = "SELECT * " \
                                    "FROM `interviewer`;"

                cursor.execute(self.insert_query)
                table = cursor.fetchall()



        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return False

        else:
            self.connection.close()
            print("Successfully inserted")
            print("Connection closed ...")
            return table

    def save_title_quiz(self, title, description, type):
        self.connect_myBD()
        try:
            with self.connection.cursor() as cursor:

                self.insert_query_title_test = "INSERT INTO `quizzes_all` (title, description, type) " \
                                          f"VALUES (%s, %s, %s);"

                cursor.execute(self.insert_query_title_test, (title, description, type))
                self.connection.commit()


        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return False

        else:
            self.connection.close()
            print("Successfully inserted")
            print("Connection closed ...")
            return True

    def save_answers_options(self, answers_options, number_right_answers, right_answer):
        self.connect_myBD()
        try:
            with self.connection.cursor() as cursor:

                self.insert_query = "INSERT INTO `answers` (answers_options, number_right_answers, right_answer) " \
                                               f"VALUES (%s, %s, %s);"

                cursor.execute(self.insert_query, (answers_options, number_right_answers, right_answer))
                self.connection.commit()


        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return False

        else:
            self.connection.close()
            print("Successfully inserted")
            print("Connection closed ...")
            return True

    def get_answers_id(self, answers_options, number_right_answers, right_answer): # переписать
        self.connect_myBD()
        try:
            with self.connection.cursor() as cursor:

                self.insert_query = "SELECT id_answers" \
                                    "FROM testing_system.answers" \
                                    f"WHERE JSON_CONTAINS(`answers_options`, (%s))" \
                                    f"AND JSON_CONTAINS(`number_right_answers`, (%s))" \
                                    f"AND `right_answer` = (%s);"

                cursor.execute(self.insert_query, (answers_options, number_right_answers, right_answer))
                id_answer = cursor.fetchone()


        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return None

        else:
            self.connection.close()
            print("Successfully inserted")
            print("Connection closed ...")
            return id_answer


    def save_one_question(self, tittle, is_closed, name_question, answers_options, number_right_answers, right_answer): # переписать
        self.connect_myBD()
        self.save_answers_options(name_question, answers_options, number_right_answers)
        id_answer = self.get_answers_id(name_question, answers_options, number_right_answers)

        try:
            with self.connection.cursor() as cursor:

                self.insert_query_title_test = "INSERT INTO `test_questions` (is_closed, name_queshtion) " \
                                          f"VALUES (%s, %s, %s);"

                cursor.execute(self.insert_query_title_test, (None, None, type))
                self.connection.commit()


        except Exception as e:
            print("Failed to:", e)
            print("Connection closed ...")
            return False

        else:
            self.connection.close()
            print("Successfully inserted")
            print("Connection closed ...")
            return True

