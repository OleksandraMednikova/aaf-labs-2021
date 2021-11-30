class CommandParser():

    def change_quote(self, line):
        quotes = []
        for i in range(len(line)):
            if line[i] == '"':
                quotes.append(i)

        new_line = ''
        f_quote = 0
        l_quote = 0
        is_in_quotes = False 
        replace_quotes = {}

        for i in quotes:
            l_quote = i
            if not is_in_quotes:
                new_line += line[f_quote:l_quote]
            else:
                temp = '@_' + str(i)
                replace_quotes[temp] = line[f_quote:l_quote]
                new_line += temp
            
            is_in_quotes = not is_in_quotes
            f_quote = l_quote + 1

        new_line +=  line[f_quote:]
        return new_line, replace_quotes
            
    def parse(self, query_line):
        changed_quote_info = self.change_quote(query_line)
        new_line = changed_quote_info[0]
        new_line_parts = new_line.split()
        replace_quotes = changed_quote_info[1]

        if new_line_parts[0].upper() == 'CREATE':
            if len(new_line_parts) == 2 and len(replace_quotes) == 0:
                return CreateCommand(new_line_parts[1])
            else:
                print(InvalidCommand())
                return InvalidCommand()

        if new_line_parts[0].upper() == 'INSERT':
            if len(new_line_parts) == 3 and len(replace_quotes) == 1:
                return InsertCommand(new_line_parts[1], replace_quotes[new_line_parts[2]])
            else:
                print(InvalidCommand())
                return InvalidCommand()

        if new_line_parts[0].upper() == 'PRINT_INDEX':
            if len(new_line_parts) == 2 and len(replace_quotes) == 0:
                return PrintIndexCommand(new_line_parts[1])
            else:
                print(InvalidCommand())
                return InvalidCommand()

        if new_line_parts[0].upper() == 'SEARCH':
            if len(new_line_parts) == 2 and len(replace_quotes) == 0:
                return SearchCommand(new_line_parts[1])
            elif len(new_line_parts) > 2:
                if new_line_parts[2].upper() == 'WHERE':
                    if len(new_line_parts) == 4 and len(replace_quotes) == 1:
                        return SearchCommand(new_line_parts[1], [replace_quotes[new_line_parts[3]]])
                    elif len(new_line_parts) == 6 and len(replace_quotes) == 2:
                        return SearchCommand(new_line_parts[1], [replace_quotes[new_line_parts[3]], new_line_parts[4], replace_quotes[new_line_parts[5]]])
            else:
                print(InvalidCommand())
                return InvalidCommand()
        
        print(InvalidCommand())
        return InvalidCommand()
        
class InvalidCommand():
    def is_valid():
        return False
    
    def __repr__(self):
        return 'Input data is not correct!\n'

class CreateCommand():
    def __init__(self, table_name):
        self.table_name = table_name

    def __repr__(self):
        return 'CREATE ' + self.table_name + ';'

class InsertCommand():
    def __init__(self, table_name, document):
        self.table_name = table_name
        self.document = document
    
    def __repr__(self):
        return 'INSERT ' + self.table_name + ' ' + '"' + self.document + '"' + ';'

class PrintIndexCommand():
    def __init__(self, table_name):
        self.table_name = table_name
    
    def __repr__(self):
        return 'PRINT_INDEX ' + self.table_name + ';'

class SearchCommand():
    def __init__(self, table_name, where_part=None):
        self.table_name = table_name

        if where_part == None:
            self.type = 'simple_where'

        elif len(where_part) == 1:
            self.type = 'one_word_where'
            self.word = where_part[0]

        elif len(where_part) == 3:
            if where_part[1] == '-':
                self.type = 'interval_where'
                self.words = [where_part[0], where_part[2]]
            else:
                self.type = 'distance_where'
                self.words = [where_part[0], where_part[2]]
                self.distance = int(where_part[1][1:-1])
    
    def __repr__(self) -> str:
        if self.type == 'simple_where':
            return 'SEARCH ' + self.table_name + ';'
        elif self.type == 'one_word_where':
            return 'SEARCH ' + self.table_name + ' ' + 'WHERE ' + '"' + self.word + '"' + ';'
        elif self.type == 'interval_where':
            return 'SEARCH ' + self.table_name + ' ' + 'WHERE ' + '"' + self.words[0] + '"' + ' ' + '- ' + '"' + self.words[1] + '"' + ';'
        elif self.type == 'distance_where':
            return 'SEARCH ' + self.table_name + ' ' + 'WHERE ' + '"' + self.words[0] + '"' + ' ' + '<' + str(self.distance) + '> ' + '"' + self.words[1] + '"' + ';'