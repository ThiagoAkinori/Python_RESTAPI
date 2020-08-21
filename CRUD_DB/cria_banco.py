import sqlite3

connection = sqlite3.connect('banco.db')
cursor = connection.cursor()


cria_tabela = '''
create table if not exists hoteis (
    hotel_id text PRIMARY KEY,
    nome text,
    estrelas real,
    diaria real,
    cidade text
)
'''

cria_hotel = '''
    insert into hoteis values (
        'alpha', 'Alpha Hotel', 4.3 , 345.3, 'Rio de Janeiro'
    )
'''

cursor.execute(cria_tabela)
cursor.execute(cria_hotel)

connection.commit()
connection.close()