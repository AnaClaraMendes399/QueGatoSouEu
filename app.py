from flask import Flask, render_template, redirect, request, flash
import requests

ENDPOINT_API = "https://api.thecatapi.com/v1/images/search"

app = Flask(__name__)
app.secret_key = 'chave-secreta-aqui'

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/cat', methods=['GET','POST'])
def gato():
    if request.method == 'GET':
        return redirect('/')
    
    nome = request.form.get('nome', '').strip()
    
    if not nome:
        flash("ERRO! Você precisa digitar o nome!")
        return redirect('/')
    
    if any(char.isdigit() for char in nome):
        flash("ERRO! O nome não pode conter números!")
        return redirect('/')
    
    if len(nome) < 2:
        flash("ERRO! O nome deve ter pelo menos 2 letras!")
        return redirect('/')
    
    nome_formatado = nome.title()
    
    resposta = requests.get(ENDPOINT_API)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        url_imagem = dados[0]['url']
    else:
        flash("ERRO! Os gatos estão dormindo. Volte mais tarde.")
        return redirect('/')
    
    return render_template('index.html', nome=nome_formatado, url_imagem=url_imagem)

if __name__ == '__main__':
    app.run(debug=True)