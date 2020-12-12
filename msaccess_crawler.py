import pyodbc

""" This simplistic tool merely connects to an MS Access database, runs through the talbes 
    and creates a .txt document with DDL statements in PostgresSQL format. As a comment 
    section above each SQL statement, it will do the rowcount. In this variant it ignores 
    any 'remote' tables (SYNONYM tables in Access' dictionary) since obdc drops connection once
    we try and do the rowcount. Yet if you absolutely need the remote talbes structure

    Please note : some data types (well might be a lot of them actually) need manual translation 
    from MS Access to Postgres (like GUID to UUID).
    """

db_path = str(input('Full path to the MS Access db to process please: '))  # >> C:\Users\dshtom\Documents\TestDB.accdb

try:
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s;' % db_path)
except Exception as e:
    print("""\n Probably something is wrong with the path you specified. Make sure it looks like this: \
     C:\somefolder\DBName.accdb   (no quotes) \n ERROR : """ + str(e))

cursor = cursor2 = conn.cursor()

table_dict = {i[2]: i[-2] for i in cursor.tables() if i[-2] != 'SYSTEM TABLE'}
print(f'Tables found in Access : {table_dict.keys()}\n')

sql_output = []

print('Generating DDLs for tables..\n')
for table, type in table_dict.items():  # GENERATING THE CREATE TABLE SQL STATEMENT LIST

    if type == 'TABLE':  # IGNORING REMOTE TABLES SINCE DOING A COUNT(*) CAN DROP THE ODBC CONNECTION ON LARGE ONES
        rowcount = cursor2.execute(f'SELECT COUNT(*) FROM {table};').fetchall()
        repl = ['[', ']', '(', ')', ',']
        for r in repl:
            rowcount = str(rowcount).replace(r, '')
    else:
        rowcount = None

    sql_generator = f'-- TABLE : {table} - TYPE : {"REMOTE" if type == "SYNONYM" else type}\
        {" - ROWCOUNT :" if rowcount else ""} {rowcount if rowcount else ""}\
        \nCREATE TABLE IF NOT EXISTS {table} ( \n'
    column_list = list(cursor.columns(table=table))
    for field in column_list:
        sql_generator += f'{field[3]}' \
                         f' {"SERIAL" if field[5] == "COUNTER" else field[5]}({255 if field[6] == 1073741823 else field[6]}) ' \
                         f' {"NOT NULL" if field[17] == "NO" else ""} {"," if field != column_list[-1] else ");"} \n'
    sql_output.append(sql_generator)

    filename = db_path.split('\\')[-1].split('.')[0]

with open(db_path.split('\\')[-1].split('.')[0] + '.txt', 'w') as output_file:
    for expression in sql_output:
        output_file.write(expression + '\n')

print('Finished.')

