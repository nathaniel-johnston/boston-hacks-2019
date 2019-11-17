import psycopg2


class DBConnection(object):

    def __init__(self, params):
        try:
            self.conn = psycopg2.connect(host=params["host"], user=params["user"], password=params["password"],
                                         dbname=params["database"])
        except:
            print("Unable to connect to the database")

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def execute(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def close(self):
        self.conn.close()
