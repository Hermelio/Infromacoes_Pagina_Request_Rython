import mysql.connector 

con = mysql.connector.connect(user='root',password='Hermelio@123', host='127.0.0.1',database='agenda')
cursor  = con.cursor()

inserir = ("insert into contatos (nome, telefone, celular) " "values ('Pateta', '(27)1111-1111', '(27)12345-3333')")


cursor.execute(inserir)
con.commit()
cursor.close()
con.close()