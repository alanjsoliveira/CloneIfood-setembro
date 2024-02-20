from app import app
from flask import render_template
import sqlalchemy as db
from sqlalchemy import Column, String, Integer, CHAR, ForeignKey, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

conexao = db.create_engine("sqlite:///Ifood_DB.db", echo = True)
Base = declarative_base()

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


class cadastro(Base):

    __tablename__ = "cadastro"
    
    email = Column("email", VARCHAR, primary_key=True )

    
    def __init__(self, email):
    
        self.email = email

        pass


Base.metadata.create_all(bind = conexao)

Session = sessionmaker(bind = conexao)
session = Session()

cadastro1 = cadastro('testemailpeloamordedeus@gmail.com')
session.add(cadastro1)
session.commit()

#, 22203300, 'peloamordedeusroda', 'casadosenhor', '777', 'b', 'osenhoréluzenadamefaltará'
#, tel, nome, endereco, num_endereco, complemento, senha
#         self.tel = tel
        # self.nome = nome
        # self.endereco = endereco
        # self.num_endero = num_endereco
        # self.complemento = complemento
        # self.senha = senha