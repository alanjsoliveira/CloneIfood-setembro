from app import app 
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return 'Entre em http://127.0.0.1:5000/entrar'

@app.route('/entrar')
def entrar():
    return render_template('cadastro.html')

@app.route('/entrar/celular')
def entrar_cel():
    return render_template('Cadastro_celular.html')

@app.route('/entrar/email')
def entrar_email():
    return render_template('Cadastro_e-mail.html')