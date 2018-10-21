import csv, sqlite3

class DataAccess():

    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def LoadCSVTable(self, tableName, cols):
        if len(tableName) <= 0 or len(cols) <= 0:
            raise ValueError
            
        colNames = ', '.join(['%s' % i[0] for i in cols])
        self.cur.execute('create table %s (%s);' % (tableName, ', '.join(['%s %s' % (i[0], i[1]) for i in cols])))
        with open('../database/%s.csv' % tableName) as f:
            reader = csv.reader(f)
            next(reader) # skip col names
            values = [tuple(row) for row in reader]
            params = ('?,' + '?,'.join(' ' * len(cols))).rstrip(', ')

        self.cur.executemany('insert into accounts (%s) values (%s);' % (colNames, params), values)
        self.conn.commit()