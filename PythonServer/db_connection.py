import psycopg2
import os


class DBConnection(object):

    def __init__(self, params):
        if os.environ.get('GAE_ENV') == 'standard':
            host = '/cloudsql/{}'.format(params["connection_name"])
        else:
            host = "localhost"
        try:
            self.conn = psycopg2.connect(host=host, user=params["user"], password=params["password"],
                                         dbname=params["database"])
        except:
            print("Unable to connect to the database")

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur.fetchall()

    def execute(self, query, returning=False):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()
        if returning:
            return cur.fetchone()[0]

    def close(self):
        self.conn.close()
