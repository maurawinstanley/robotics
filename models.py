import sqlite3

class ColorsModel:
    

    def __init__(self):
      self.conn = sqlite3.connect('colors.db')
      self.TABLENAME = "Colors"

    def create(self, color):
      query = f'insert into {self.TABLENAME} ' \
              f'(color) ' \
              f'values ("{color}")'
      
      result = self.conn.execute(query)
      print(result)
      return result
   # Similarly add functions to select, delete and update todo

















