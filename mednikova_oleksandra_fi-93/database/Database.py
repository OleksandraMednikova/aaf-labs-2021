import re
from binary_tree.BinaryTree import BinaryTree
from command_parser.CommandParser import CommandParser, CreateCommand, InsertCommand, PrintIndexCommand, SearchCommand

class Database():
    def __init__(self):
        self.parser = CommandParser()
        self.tables = {}
    
    def create(self):
        if self.query.table_name not in self.tables:
            self.tables[self.query.table_name] = Table(self.query.table_name)
            return self.query.table_name
        else:
            return None

    def insert(self):
        if self.query.table_name in self.tables:
            add = self.tables[self.query.table_name].add_document(self.query.document)
            return self.query.table_name
        else:
            return None

    def print_index(self):
        if self.query.table_name in self.tables:
            for value, data in self.tables[self.query.table_name].indeces:
                print('"' + value + '":')
                for k, v in data.items():
                    print(' ' + str(k) + ' -> ' + str(v))
            return True
        else:
            return None

    def search(self):
        if self.query.table_name in self.tables:
            if self.query.type == 'simple_where':
                for row in self.tables[self.query.table_name].rows:
                    print('"' + row + '"')
                return True
            elif self.query.type == 'one_word_where':
                word_lower = self.query.word.lower()
                if word_lower in self.tables[self.query.table_name].indeces:
                    temp_node = self.tables[self.query.table_name].indeces.get(word_lower)
                    for d_id in temp_node.data.keys():
                        print('"' + self.tables[self.query.table_name].rows[d_id] + '"')
                    return True
            elif self.query.type == 'interval_where':
                ids = set()
                self.query.words.sort()
                less = self.query.words[0]
                more = self.query.words[1]
                self.tables[self.query.table_name].indeces.interval_search(less, more, ids, self.tables[self.query.table_name].indeces.root)
                for d_id in ids:
                    print('"' + self.tables[self.query.table_name].rows[d_id] + '"')
                return True
            elif self.query.type == 'distance_where':
                word_lower1 = self.query.words[0].lower()
                word_lower2 = self.query.words[1].lower()
                if (word_lower1 in self.tables[self.query.table_name].indeces) and (word_lower2 in self.tables[self.query.table_name].indeces):
                    temp_data1 = self.tables[self.query.table_name].indeces.get(word_lower1).data
                    temp_data2 = self.tables[self.query.table_name].indeces.get(word_lower2).data
                    result = set()
                    for k1, v1 in temp_data1.items():
                        if k1 in temp_data2.keys():
                            v2 = temp_data2[k1]
                            for num in v1:
                                if (num + self.query.distance) in v2 or (num - self.query.distance) in v2:
                                    result.add(k1)
                                    break
                    for d_id in result:
                        print('"' + self.tables[self.query.table_name].rows[d_id] + '"')
                    if len(result) != 0:
                        return True
        else:
            return self.query.table_name

    def execute(self, command):
        self.query = self.parser.parse(command)
        if type(self.query) == CreateCommand:
            result = self.create()
            if result is None:
                print('ERROR: This table has already been created!\n')
            else:
                print('Collection ' + result + ' has been created.\n')

        elif type(self.query) == InsertCommand:
            result = self.insert()
            if result is None:
                print('ERROR: InsertCommand has not been executed!\n')
            else:
                print('Document has been added to ' + result + '.\n')

        elif type(self.query) == PrintIndexCommand:
            result = self.print_index()
            if result:
                print()
            else:
                print('ERROR: This collection cannot be printed!\n')

        elif type(self.query) == SearchCommand:
            result = self.search()
            if result is True:
                print()
            else:
                print('ERROR: There are no such documents in the database!\n')

class Table():
    def __init__(self, table_name):
        self.table_name = table_name
        self.rows = []
        self.indeces = BinaryTree()

    def add_document(self, document):
        self.rows.append(document)
        doc_id = len(self.rows) - 1
        words = re.findall('[a-zA-Z0-9_]+', document) 
        temp = {}
        for word in words:
            if word.lower() not in self.indeces:
                self.indeces.add(word.lower(), {})
            if word.lower() not in temp:
                temp[word.lower()] = []
        for i in range(len(words)):
            temp[words[i].lower()].append(i)
        for word in words:
            self.indeces.get(word.lower()).data[doc_id] = temp[word.lower()]
        return self.indeces

