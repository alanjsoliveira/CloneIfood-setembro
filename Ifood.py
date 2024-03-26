from flask import Flask,render_template,request, jsonify, redirect, url_for, session
import psycopg2 as pg
import numpy as np
from twilio.rest import Client
import random, secrets
import smtplib
import email.message

app = Flask(__name__)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

conn = pg.connect(database = "Ifood", host = "localhost", user = "postgres", password = "admin")

app.secret_key = secrets.token_bytes(16)

Email = False
Celular = False
login = False
nome = None



@app.route("/home")
def pagina_inicial():
    
    if Email is not False:
            global nome
            cur = conn.cursor()
            cur.execute(f'SELECT nome FROM "Usuario" where email = {emailFinal}')
            nome = cur.fetchone() 
            nome = nome[0].split()
            nome = nome[0]
            
            cur.close()
            return render_template("home.html", login = True, nome = nome ,endereco = "teste")

    return render_template('home.html', login = False)


@app.route("/")
def home():
    return redirect('/home')


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

                emailCli = session['emailCli']
                global emailFinal
                emailFinal = f"'{emailCli}'"

                cur = conn.cursor()
                
                cur.execute(f'SELECT email FROM "Usuario" where email = {emailFinal}')

                registro = cur.fetchall()
                
                print(registro)
                if len(registro) != 0:
                    cur.close()
                    return redirect('/home')

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


@app.route("/minha-conta/dados-cadastrais/")
def minha_conta():
    if Email == False:
        return redirect(url_for('home'))
    global nome
    
    return render_template("Página_dados_cadastrais.html",login = True ,nome=nome, endereco = "teste")

@app.route("/minha-conta/informacao-pessoais", methods=['POST','GET'])
def minha_conta_info_pessoal():
    if Email == False:
        return redirect(url_for('home'))
    

    if request.method == 'POST':
        
        nomeCli = request.form.get("mundanca_nome")
        cpf = request.form.get("mundanca_cpf")
        table = '"Usuario"'

        cur = conn.cursor()
                
        cur.execute(f"UPDATE {table} SET nome='{nomeCli}', cpf='{cpf}' WHERE email={emailFinal};")


        conn.commit()
        cur.close()






    global nome
    return render_template("Pagina_dados_cadastrais_info_pessoal.html", nome=nome, login = True, endereco = 'teste')

@app.route("/bebidas")
def pagina_bebidas():
    return render_template("Página_bebidas.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)