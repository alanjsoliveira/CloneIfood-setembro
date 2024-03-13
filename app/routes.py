from app import app
from flask import Flask,render_template,request, jsonify, redirect, url_for, session
import psycopg2 as pg
import numpy as np
from twilio.rest import Client
import random, secrets
import smtplib
import email.message

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

conn = pg.connect(database = "ifood", host = "localhost", user = "postgres", password = "admin")

app.secret_key = secrets.token_bytes(16)

Email = False
Celular = False

@app.route("/", endpoint='home')
def pagina_inicial():

    for iten in session:
        session.pop(iten)
    return render_template("home.html")

@app.route("/cadastro")
def cadastro():



    return render_template("cadastro.html")

@app.route("/cadastro_celular",methods=['POST','GET'])
def cadastro_celular():

    if request.method == 'POST':
        print(request.form['phoneNumber'])
        session['telefone'] = request.form['phoneNumber']

        session['codAcessCelular'] = random.randrange(100000, 999999, 6)

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f'Seu código de verificação é {session["codAcessCelular"]}. Para sua segurança, não o compartilhe.',
            to=f'whatsapp:+55{session["telefone"]}'
            )

        print(message.sid)
        print(session['telefone'])

        global Celular
        Celular = True
        return render_template("/código_de_acesso.html")


    return render_template("cadastro_celular.html")

@app.route("/cadastro_email", methods=['POST', 'GET'])
def cadastro_email():

    if request.method == 'POST':
        session['emailCli']  = request.form['email']
        session['codAcessEmail']= random.randrange(100000, 999999, 6)


        msg = email.message.Message()
        msg['Subject'] = "Código de acesso"
        msg['From'] = 'ifooddossistematicos@gmail.com'
        msg['To'] = session['emailCli']
        password = 'rahq bsnc auyn jvzc' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(str(session['codAcessEmail']))

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        # Login Credentials for sending the mail
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')
        global Email
        Email = True
        return render_template("código_de_acesso.html")

    return render_template("cadastro_e-mail.html")


@app.route("/código_de_acesso", methods=['POST','GET'])
def codigo_verificacao():
    
    if Email == False:
        if request.method == 'POST':
            accessCodeCelular = request.form.get('accessCode')
            
        if int(accessCodeCelular) == session['codAcessCelular']:
            return render_template('cadastro_e-mail.html')
            
        else:
            return render_template("código_de_acesso.html", codErrado = True)

    elif Celular == False:
        if request.method == 'POST':
            accessCodeEmail = request.form.get('accessCode')
            
            if int(accessCodeEmail) == session['codAcessEmail']:
                return render_template('cadastro_celular.html')
            
            else:
                return render_template("código_de_acesso.html", codErrado = True)
            
    
    else:
        return render_template("registro_Nome_Cpf.html")

            
    return render_template("código_de_acesso.html")

@app.route("/registroFinal", methods=['POST','GET'])
def teste():
    if request.method == 'POST':
        session['nome']  = request.form['nome']
        session['cpf'] = request.form['cpf']


        cur = conn.cursor()

        table = '"Usuario"'
        emailCli = session['emailCli'] 
        nomeCli = session['nome']
        cpfCli = session ['cpf']
        celCli = session['telefone']

        SqlStr =f"INSERT INTO {table} (email, nome, cpf, telefone, endereco) VALUES ('{emailCli}', '{nomeCli}',{cpfCli},{celCli},'testeendereco');"
        print(SqlStr)
        cur.execute(f"{SqlStr}")
        conn.commit()

        cur.close()


        return render_template("home.html")

    return render_template('registro_Nome_Cpf.html')

@app.route("/bebidas")
def pagina_bebidas():
    return render_template("Página_bebidas.html")


