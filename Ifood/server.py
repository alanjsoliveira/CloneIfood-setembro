from flask import Flask,render_template,request, jsonify, redirect, url_for
import psycopg2 as pg
import numpy as np
from twilio.rest import Client
import random

account_sid = 'ACbfd57f67730c9f2493b91976826e59ad'
auth_token = 'f7716047afe084b327743331e448e43e'
client = Client(account_sid, auth_token)

conn = pg.connect(
    host="localhost",
    user="postgres",
    password="Ml304210?",
    port="5432",
    dbname="Ifood.bd"
)

app = Flask(__name__)

@app.route("/", endpoint='home')
def pagina_inicial():
    return render_template("teste_pagina2.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro_celular",methods=['POST','GET'])
def cadastro_celular():
    if request.method == "POST":
        telefone = request.form['phoneNumber']
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TBIF_CADASTRO(Telefone) VALUES(%s)",(telefone,))
            conn.commit()
            cursor.close()
        except Exception as e:
            print("Erro:",e)
            conn.rollback()
        finally:
            cursor.close()
    return render_template("cadastro_celular.html")

@app.route("/cadastro_email", methods=['POST', 'GET'])
def cadastro_email():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
        else:
            email = request.form.get('email')

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM TBIF_CADASTRO WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            return jsonify({'error': 'E-mail já cadastrado'}), 200
        else:
            try:
                cursor.execute("INSERT INTO TBIF_CADASTRO(Email) VALUES(%s)", (email,))
                conn.commit()
                return jsonify({'message': 'Cadastro realizado com sucesso'}), 200
            except Exception as e:
                print("Erro:", e)
                conn.rollback()
                return jsonify({'error': 'Erro ao cadastrar o e-mail'}), 500
            finally:
                cursor.close()

    return render_template("cadastro_e-mail.html")



@app.route("/codigo_verificacao", methods=['POST','GET'])
def codigo_verificacao():

    lista_cod = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(lista_cod)
    codigo_ver = lista_cod[:6]
    codigo1 = np.array(codigo_ver)

    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f'Seu código de verificação é {codigo1}. Para sua segurança, não o compartilhe.',
    to='whatsapp:+5511997366122'
    )

    print(message.sid)


    if request.method == 'POST':
        codigo_str = request.form.get('accessCode')
        if codigo_str and len(codigo_str) == 6 and codigo_str.isdigit():
            codigo = np.array([int(digit) for digit in codigo_str])
            
            if np.array_equal(codigo, codigo1):
                return redirect(url_for('home'))
            else:
                return "Código incorreto. Por favor, tente novamente."
        else:
            return "O código de acesso deve ser uma sequência de 6 números."
    return render_template("código_de_acesso.html")



@app.route("/bebidas")
def pagina_bebidas():
    return render_template("Página_bebidas.html")


if __name__ == '__main__':
    app.run(debug=True)

