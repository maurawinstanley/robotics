import sqlite3
import sys

class ColorsModel:
    

    def __init__(self):
      self.conn = sqlite3.connect('colors.db')
      self.TABLENAME = "Colors"
      #print(self.conn, " is the conn")

    def create(self, color):
      query = f'insert into {self.TABLENAME} ' \
              f'values ("{color}")'
      
      result = self.conn.execute(query)
      self.conn.commit()
      print(query)
      print('Hello world!', file=sys.stderr)
      return result

    def get(self):
      query = f'select * from {self.TABLENAME}'
      result = self.conn.execute(query)
      print("result: ")
      results = ""
      for row in result:
        results += str(row).strip("(").strip(")").strip(",") + "\n\n"
      return results
   # Similarly add functions to select, delete and update todo

















