from app import app
from flask import Flask,render_template,request, jsonify, redirect, url_for, session
import psycopg2 as pg
import numpy as np
from twilio.rest import Client
import random, secrets

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

conn = pg.connect(database = "ifood", host = "localhost", user = "postgres", password = "admin")

app.secret_key = secrets.token_bytes(16)

@app.route("/", endpoint='home')
def pagina_inicial():


    return render_template("teste_pagina2.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro_celular",methods=['POST','GET'])
def cadastro_celular():

    if 'telefone' in session:
        session.pop('telefone', None)

    if request.method == 'POST':
        print(request.form['phoneNumber'])
        session['telefone'] = request.form['phoneNumber']
        return render_template("/código_de_acesso.html")


    return render_template("cadastro_celular.html")

@app.route("/cadastro_email", methods=['POST', 'GET'])
def cadastro_email():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
        else:
            email = request.form.get('email')


    return render_template("cadastro_e-mail.html")



@app.route("/código_de_acesso", methods=['POST','GET'])
def codigo_verificacao():

    lista_cod = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(lista_cod)
    codigo_ver = lista_cod[:6]
    codigo1 = np.array(codigo_ver)


    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body=f'Seu código de verificação é {codigo1}. Para sua segurança, não o compartilhe.',
    to=f'whatsapp:+55{session["telefone"]}'
    )

    print(message.sid)
    print(session['telefone'])



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

