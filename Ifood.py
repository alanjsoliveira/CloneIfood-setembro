from flask import Flask,render_template,request, jsonify, redirect, url_for, session
from flask_cors import CORS
import psycopg2 as pg
import numpy as np
from twilio.rest import Client
import random, secrets
import smtplib
import email.message
import geocoder
import googlemaps
import time
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import date

data_atual = date.today()
data_em_texto = '{}/{}/{}'.format(data_atual.day, data_atual.month,data_atual.year)


app = Flask(__name__)
CORS(app)

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

conn = pg.connect(database = "ifood", host = "localhost", user = "postgres", password = "1234")

app.secret_key = secrets.token_bytes(16)
gmaps = googlemaps.Client(key='AIzaSyAPR7_-eTwAM_AP864F9G0Yue8aV_cbrLU')

Email = False
Celular = False
login = False
nome = None
enderecoCli = None
dados_carrinho = None



@app.route("/home")
def pagina_inicial():
    
    if Email is not False:
            global nome
            global enderecoCli
        

            cur = conn.cursor()
            cur.execute(f'SELECT nome FROM "Usuario" where email = {emailFinal}')
            nome = cur.fetchone() 
            nome = nome[0].split()
            nome = nome[0]
            cur.close()

            cur = conn.cursor()
            cur.execute(f'SELECT endereco FROM "Usuario" where email = {emailFinal}')
            endereco = cur.fetchone()
            enderecoInt = endereco[0].split(',')
            enderecoCli = enderecoInt[1]
            cur.close()
            return render_template("home.html", login = True, nome = nome ,endereco = enderecoCli)

    return render_template('página-inicial.html', login = False)


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

        

        return redirect("/localizacao")

            
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
        enderecoCli = session['endereco']

        SqlStr =f"INSERT INTO {table} (email, nome, cpf, telefone, endereco) VALUES ('{emailCli}', '{nomeCli}',{cpfCli},{celCli},'{enderecoCli}');"
        print(SqlStr)
        cur.execute(f"{SqlStr}")
        conn.commit()

        cur.close()


        return redirect("/home")

    return render_template('registro_Nome_Cpf.html')


@app.route("/minha-conta/dados-cadastrais/")
def minha_conta():
    if Email == False:
        return redirect('/home')
    global nome
    
    return render_template("Página_dados_cadastrais.html",login = True ,nome=nome, endereco = enderecoCli)

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
    return render_template("Pagina_dados_cadastrais_info_pessoal.html", nome=nome, login = True, endereco = enderecoCli)


@app.route("/localizacao", methods=["POST", "GET"])
def localizacao():


        current_location = obter_endereco()
        if current_location:
            latitude = current_location[0]
            longitude = current_location[1]

            
            global numero_rua
            global cep
            address_info = get_address(latitude, longitude)
            session['endereco'] = address_info['formatted_address']
            numero_rua = address_info['street_number']
            cep = address_info['postal_code']


            if address_info:
                print("Endereço completo:", session['endereco'] )
                print("Número da rua:", numero_rua )
                print("CEP:", cep)
            else:
                print("Não foi possível obter informações do endereço.")
         
        
            print('Foi POST')
            return redirect('/registroFinal')
        


@app.route("/Restaurante", methods=['GET', 'POST'])
def Restaurante():

    # if request.method == 'POST':
    #     redirect('/pagamento')
       

    return render_template("Pagina_Restaurante.html", nome=nome, login = True, endereco = enderecoCli)
    

@app.route("/favoritos", methods=['POST','GET'])
def favoritos():
    return render_template("favoritos.html")


@app.route("/mcdonalds", methods=['POST','GET'])
def rest():
    nome = 'Mc Donalds'
    foto = 'static/img/Mcdonalds.png'
    return render_template("rest.html", nome = nome, foto = foto)

@app.route("/kfc", methods=['POST','GET'])
def rest2():
    nome = 'KFC'
    foto = 'static/img/KFC.png'
    return render_template("rest.html", nome = nome, foto = foto)

@app.route("/burguerking", methods=['POST','GET'])
def rest3():
    nome = 'Burguer King'
    foto = 'static/img/Buguer_King.png'
    return render_template("rest.html", nome = nome, foto = foto)

@app.route('/carrinho', methods=['POST'])
def receber_dados_carrinho():
    
    global dados_carrinho
    dados_carrinho = request.json

    return jsonify({"message": "Dados do carrinho recebidos com sucesso!"})


@app.route('/pagamento', methods=['POST', 'GET'])
def pagamentos():

    global dados_carrinho
    carrinho = dados_carrinho
    print(carrinho)
    valor_total = carrinho['totalAmount']
    prod = carrinho ['produtos']
    qtditens = len(prod)
    listaItensCarrinho = []
    numItem = []


    for iten in prod:
        listaItensCarrinho.append(iten['nome'])
        numItem.append(iten['quantidade'])

    print(dados_carrinho)


    return render_template('pagamento.html', carrinho = carrinho, qtditens = qtditens, listaItens = listaItensCarrinho, numItem = numItem, valor_total = valor_total, login = True, nome = nome ,endereco = enderecoCli)


@app.route('/Status-do-pedido', methods = ['GET'])
def status():
    global dados_carrinho
    carrinho = dados_carrinho
    
    table = '"Usuario"'

    cur = conn.cursor()
                    
    cur.execute(f"SELECT telefone FROM {table}  WHERE email= {emailFinal};")
    numcli = cur.fetchone()

    message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=f'Seu pedido foi pago com sucesso',
                to=f'whatsapp:+55{numcli[0]}'
                )

    cur = conn.cursor()
                    
    cur.execute(f"SELECT nome, cpf FROM {table}  WHERE email= {emailFinal};")
    nome, cpf = cur.fetchone()

    criar_nfe(carrinho, nome, cpf)


    msg = MIMEMultipart()
    msg['Subject'] = "Nota Fiscal eletronica"
    msg['From'] = 'ifooddossistematicos@gmail.com'
    msg['To'] = session['emailCli']
    password = 'rahq bsnc auyn jvzc' 

    msg.attach(MIMEText('Nota Fiscal Eletronica','html'))

    msg.add_header('Content-Type', 'text/html')
  
  
    #Abrimos o arquivo em modo leitura e binary 
    cam_arquivo = "NFe.pdf"
    attchment = open(cam_arquivo,'rb')

    #Lemos o arquivo no modo binario e jogamos codificado em base 64 (que é o que o e-mail precisa )
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attchment.read())
    encoders.encode_base64(att)

    #ADCIONAMOS o cabeçalho no tipo anexo de email 
    att.add_header('Content-Disposition', f'attachment; filename= NFe Dos Sistematicos.pdf')
    #fechamos o arquivo 
    attchment.close()

    #colocamos o anexo no corpo do e-mail 
    msg.attach(att)


    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')




    valor_total = carrinho['totalAmount']
    prod = carrinho ['produtos']
    qtditens = len(prod)
    listaItensCarrinho = []
    numItem = []


    for iten in prod:
        listaItensCarrinho.append(iten['nome'])
        numItem.append(iten['quantidade'])

    print(listaItensCarrinho, numItem)
    mandamsg()

    return render_template('status_pedido.html', carrinho = carrinho, qtditens = qtditens, listaItens = listaItensCarrinho, numItem = numItem, valor_total = valor_total, login = True, nome = nome ,endereco = enderecoCli)






def obter_endereco():
    location = geocoder.ip('me')
    if location.ok:
        return location.latlng 
    else:
        print("Erro ao obter localização em tempo real.")
        return None

def get_address(lat, lng):
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))

    if reverse_geocode_result:
        result = reverse_geocode_result[0]
        formatted_address = result['formatted_address']
        street_number = None
        postal_code = None
        for component in result['address_components']:
            if 'street_number' in component['types']:
                street_number = component['long_name']
            elif 'postal_code' in component['types']:
                postal_code = component['long_name']
        
        return {
            'formatted_address': formatted_address,
            'street_number': street_number,
            'postal_code': postal_code
        }
    else:
        return None 


def mandamsg():
    Timer(5, msgwpp, ["Pedido em preparo"]).start()
    Timer(10, msgwpp, ["Motoboy a caminho do restaurante"]).start()
    Timer(15, msgwpp, ["Pedido saiu para entrega"]).start()
    Timer(20, msgwpp, ["Pedido a caminho"]).start()
    Timer(25, msgwpp, ["Pedido Entregue"]).start()

def msgwpp(mens):

    table = '"Usuario"'

    cur = conn.cursor()
                
    cur.execute(f"SELECT telefone FROM {table}  WHERE email= {emailFinal};")
    numcli = cur.fetchone()

    message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f'{mens}',
            to=f'whatsapp:+55{numcli[0]}'
            )

def create_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    # Cabeçalho
    canvas.setFont('Helvetica-Bold', 14)
    canvas.drawCentredString(width / 2.0, height - 0.75 * inch, "Nota Fiscal Eletrônica")
    canvas.setFont('Helvetica', 10)
    canvas.drawCentredString(width / 2.0, height - 1.0 * inch, "Emitida por: Sushi Place")
    canvas.drawCentredString(width / 2.0, height - 1.25 * inch, "CNPJ: 12.345.678/0001-99")
    canvas.drawCentredString(width / 2.0, height - 1.40 * inch, f"{data_em_texto}")

    # Rodapé
    canvas.setFont('Helvetica', 10)
   
    canvas.drawRightString(width - inch, 0.75 * inch, "www.NovaEraFood.com.br")
    canvas.restoreState()

# Função para criar o PDF
def criar_nfe(dados, nome, cpf, filename="NFe.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']

    centered_style = ParagraphStyle(
        name='Centered',
        parent=styles['Normal'],
        alignment=1,  # 1 is center alignment
        fontSize=12
    )

    # Adiciona título e dados do cliente
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph(f"Nome: {nome}", centered_style))
    elements.append(Paragraph(f"CPF: {cpf}", centered_style))
    elements.append(Spacer(1, 0.2 * inch))  # Espaço

    # Tabela de produtos
    data = [['Produto', 'Preço Unitário', 'Quantidade', 'Total']]

    for produto in dados['produtos']:
        nome_prod = produto['nome']
        preco_unit = produto['preco']
        quantidade = produto['quantidade']
        total = f"R${float(preco_unit.strip('R$').replace(',', '.')) * int(quantidade):.2f}".replace('.', ',')
        data.append([nome_prod, preco_unit, quantidade, total])

    # Adiciona total geral
    data.append(['', '', 'Total', f"R${dados['totalAmount']}"])

    # Cria tabela
    table = Table(data, colWidths=[2.5 * inch, 1.5 * inch, 1 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))  # Espaço

    # Construir o documento
    doc.build(elements, onFirstPage=create_header_footer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)