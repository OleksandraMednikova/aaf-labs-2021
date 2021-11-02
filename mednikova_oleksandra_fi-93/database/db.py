from command_parser.command_parser import CommandParser

class Database():
    def __init__(self):
        self.parser = CommandParser()

    def execute(self, command):
        self.query = self.parser.parse(command)
        print(self.query)