import sqlite3
import os

class DataConnector:
    def __init__(self, file=None):
        self.data_container_index = {'ID' : 0, 'title' : 1, 'desc' : 2}
        self.data_contents_index = {'ID':0, 'title':1, 'desc':2, 'container':3}
        if file is None or file == ":memory:":
            self.con = sqlite3.connect(':memory:')
            self.con.execute('CREATE TABLE containers(ID TEXT, title TEXT, desc TEXT)')
            self.con.execute('CREATE TABLE contents(ID TEXT, title TEXT, desc TEXT, container TEXT)')
        elif not os.path.exists(file):
            self.con = sqlite3.connect(file)
            self.con.execute('CREATE TABLE containers(ID TEXT, title TEXT, desc TEXT)')
            self.con.execute('CREATE TABLE contents(ID TEXT, title TEXT, desc TEXT, container TEXT)')
        else:
            self.con = sqlite3.connect(file)
        self.con.commit()


    def readvalues(self, table, len=None):
        if table == 0:
            table = 'containers'
        if table == 1:
            table = 'contents'
        return self.con.execute('SELECT * FROM containers').fetchall()

    def read_container(self, container):
        return self.con.execute('SELECT * FROM contents WHERE container = (?)', (container,)).fetchall()

    def locate_item(self, id):
        return self.con.execute('SELECT * FROM contents WHERE ID = (?)', (id,)).fetchall()

    def add_item(self, content, container, title, desc):

        self.con.execute('INSERT into contents values (?,?,?,?)', (content, title, desc, container))
        self.con.commit()

    def add_container(self, id, title, desc):
        self.con.execute('INSERT into containers values (?,?,?)', (id, title, desc))
        self.con.commit()




