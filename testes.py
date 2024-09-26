import psycopg2 as pg

conn = pg.connect(database = "Ifood", host = "localhost", user = "postgres", password = "1234")

table = '"Usuario"'

cur = conn.cursor()
                
cur.execute(f"SELECT telefone FROM {table}  WHERE email= 'alanoliveira.w@gmail.com';")
teste = cur.fetchone()
print(teste)
conn.commit()
cur.close()

print(teste) 