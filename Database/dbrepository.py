import psycopg2 as pg


class DbRepo(object):
    __conn = None
    __cursor = None

    def __init__(self):
        self.__conn = pg.connect(
            host="localhost",
            database="pychatdb",
            user="postgres",
            password="Zawer021")
        self.__cursor = self.__conn.cursor()

    def createUser(self, username, password):
        sql = """INSERT INTO users(username,password)
                 VALUES (%s,%s);"""
        data = (username, password)
        self.__cursor.execute(sql, data)
        self.__conn.commit()

    def getUser(self, username):
        sql = "SELECT * FROM users WHERE username = %s"
        self.__cursor.execute(sql, (username,))
        user = self.__cursor.fetchone()
        return user

    def createMessage(self, message, user_id):
        sql = """INSERT INTO messages(message_text ,user_id)
                         VALUES (%s,%s);"""
        data = (message, user_id)
        self.__cursor.execute(sql, data)
        self.__conn.commit()

    def getMessages(self, user_id):
        sql = """SELECT * FROM messages
                         WHERE user_id = %s"""
        self.__cursor.execute(sql, (user_id,))
        usrmessages = self.__cursor.fetchall()
        return usrmessages
