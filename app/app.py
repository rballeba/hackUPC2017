from flask import Flask, render_template, request, url_for, flash, redirect



app = Flask(__name__)
app.config.from_pyfile('config.py') # load config from this file 

@app.route('/')
def index():
    return "Hello World"

@app.route('/send', methods=['POST'])
def make_question():
    # generar url de pregunta
    # A todo el censo enviar dos votos
    pass

@app.route('/vote/<question_id>', methods=['POST', 'GET'])
def vote(question_id):
    if request.method == 'GET':
        return render_template('vote.html', question_id=question_id)
    # votar la pregunta 'question_id'
    print(1)
    form = request.form
    print(2)

    print('id {}\npw {}\nvote {}\nquestion id {}'.format(
        form['public_key'],
        form['private_key'], 
        form['vote'],
        question_id))
    print(3)

    # buscar voto que cumple form['vote']
    # crear transaccion a question
    flash('Success')
    return redirect(url_for('index'))

