from database.Database import Database

def CLI_read():
    full_line = ''
    quotes = []
    db = Database()

    while True:
        current_line = input()
        if ';' not in current_line:
            current_line += ' '
        full_line += current_line 
        
        for i in range(len(full_line)):
            if full_line[i] == '"':
                quotes.append(i)

        f_quote = 0
        l_quote = 0
        is_in_quotes = False
        final_line = ''
        is_query_done = False
        for i in quotes:
            l_quote = i
            if not is_in_quotes:
                temp = full_line[f_quote:l_quote]
                if ';' in temp:
                    final_line += ' '.join(temp[0:temp.index(';')+1].split())
                    is_query_done = True
                    break
                final_line += ' '.join(full_line[f_quote:l_quote].split()) + ' '
            else:
                final_line += full_line[f_quote:l_quote]
            is_in_quotes = not is_in_quotes
            f_quote = l_quote
        
        quotes = []
        temp = full_line[f_quote:]
        if ';' in temp:
            semicolon_index = temp.index(';')
            final_line += ' '.join(temp[:semicolon_index+1].split())
            is_query_done = True
   
        if is_query_done:
            db.execute(final_line[:-1].rstrip())
            full_line = ''
            final_line = ''
        