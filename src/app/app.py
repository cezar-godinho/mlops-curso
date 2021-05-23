from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import pickle
import os

modelo = pickle.load(open('../../models/modelo.sav', 'rb'))
colunas = ['tamanho', 'ano', 'garagem']

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)


@app.route('/')
def home():
    return 'Minha primeira API.'


@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    polaridade = tb_en.sentiment.polarity
    return "Polaridade: {}".format(polaridade)


@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    body = request.get_json()
    body_input = [body[col] for col in colunas]
    preco = modelo.predict([body_input])
    return jsonify(preco=preco[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
