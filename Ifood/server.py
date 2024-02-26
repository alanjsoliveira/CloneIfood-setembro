from flask import Flask,render_template,request, jsonify, redirect, url_for
import psycopg2 as pg

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



@app.route("/codigo_verificacao")
def codigo_verificacao():
    return render_template("código_de_acesso.html")




if __name__ == '__main__':
    app.run(debug=True)

