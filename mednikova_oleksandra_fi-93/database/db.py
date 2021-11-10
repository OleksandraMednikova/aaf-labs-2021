import re
from command_parser.command_parser import CommandParser, CreateCommand, InsertCommand, PrintIndexCommand, SearchCommand

class Database():
    def __init__(self):
        self.parser = CommandParser()
        self.tables = {}
    
    def create(self):
        if self.query.table_name not in self.tables:
            self.tables[self.query.table_name] = Table(self.query.table_name)
            print('Collection ' + self.query.table_name + ' has been created.\n')
        else:
            print('ERROR: This table has already been created!\n')

    def insert(self):
        if self.query.table_name in self.tables:
            add = self.tables[self.query.table_name].add_document(self.query.document)
            print('Document has been added to ' + self.query.table_name + '.\n')
        else:
            print('ERROR: InsertCommand has not been executed!\n')

    def print_index(self):
        if self.query.table_name in self.tables:
            for k1, v1 in self.tables[self.query.table_name].indeces.items():
                print('"' + k1 + '":')
                for k2, v2 in v1.items():
                    print(' ' + str(k2) + ' -> ' + str(v2))
            print()
        else:
            print('ERROR: This collection cannot be printed!\n')

    def search(self):
        if self.query.table_name in self.tables:
            if self.query.type == 'simple_where':
                for row in self.tables[self.query.table_name].rows:
                    print('"' + row + '"')
                print()
            elif self.query.type == 'one_word_where':
                word_lower = self.query.word.lower()
                if word_lower in self.tables[self.query.table_name].indeces.keys():
                    for d_id in self.tables[self.query.table_name].indeces[word_lower].keys():
                        print('"' + self.tables[self.query.table_name].rows[d_id] + '"')
                    print()
                else:
                    print('There is no key ' + self.query.word + ' in the collection ' + self.query.table_name + '!\n')
            elif self.query.type == 'interval_where':
                pass
            elif self.query.type == 'distance_where':
                pass
        else:
            print('ERROR: There is no ' + self.query.table_name + ' in the database!\n')

    def execute(self, command):
        self.query = self.parser.parse(command)
        if type(self.query) == CreateCommand:
            self.create()
        elif type(self.query) == InsertCommand:
            self.insert()
        elif type(self.query) == PrintIndexCommand:
            self.print_index()
        elif type(self.query) == SearchCommand:
            self.search()

class Table():
    def __init__(self, table_name):
        self.table_name = table_name
        self.rows = []
        self.indeces = {}

    def add_document(self, document):
        self.rows.append(document)
        doc_id = len(self.rows) - 1
        words = re.findall('[a-zA-Z0-9_]+', document) 
        for word in words:
            if word.lower() not in self.indeces.keys():
                self.indeces[word.lower()] = {}
        for word in words:
            self.indeces[word.lower()][doc_id] = list(get_indeces(words, word))
        return self.indeces

def get_indeces(lst, wrd):
    for i, j in enumerate(lst):
        if j == wrd:
            yield i