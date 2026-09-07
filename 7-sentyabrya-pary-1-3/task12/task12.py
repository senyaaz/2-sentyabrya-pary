import sys

class DataBase:
    lst_data = []
    FIELDS = ('id', 'name', 'old', 'salary')
    
    def insert(self, data):
        for row in data:
            values = row.split()
            row_dict = {}
            for i in range(len(self.FIELDS)):
                row_dict[self.FIELDS[i]] = values[i]
            self.lst_data.append(row_dict)
    
    def select(self, a, b):
        if b >= len(self.lst_data):
            b = len(self.lst_data) - 1
        return self.lst_data[a:b+1]


lst_in = list(map(str.strip, sys.stdin.readlines()))