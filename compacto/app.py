import os
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


Migrate(app, db)


class Tarefa(db.Model):
	__tablename__ = 'tarefas'

	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String, nullable=False)

	def __init__(self, titulo):
		self.titulo = titulo

class CriarForm(FlaskForm):

    titulo = StringField("Título da tarefa", validators=[DataRequired()])
    submit = SubmitField("Criar")

class AtualizarForm(FlaskForm):

    titulo = StringField("Título da tarefa", validators=[DataRequired()])
    submit = SubmitField("Atualizar")

@app.route('/criar', methods=['POST', 'GET'])
def criar():
	form = CriarForm()

	if form.validate_on_submit():
		nova_tarefa = Tarefa(form.titulo.data)
		db.session.add(nova_tarefa)
		db.session.commit()

		return redirect(url_for('listar'))

	return render_template('criar.html', form=form)

@app.route('/')
@app.route('/listar')
def listar():

	tarefas = Tarefa.query.all()

	return render_template('listar.html', tarefas=tarefas)


@app.route('/atualizar/<id>', methods=['POST', 'GET'])
def atualizar(id):
	form = AtualizarForm()

	tarefa = Tarefa.query.filter_by(id=id).first_or_404()

	if form.validate_on_submit():
		tarefa.titulo = form.titulo.data
		db.session.commit()

		return redirect(url_for('listar'))
	elif request.method == 'GET':
		form.titulo.data = tarefa.titulo

	return render_template('atualizar.html', form=form)


@app.route('/excluir/<id>', methods=['GET'])
def excluir(id):

	tarefa = Tarefa.query.filter_by(id=id).first_or_404()

	db.session.delete(tarefa)
	db.session.commit()

	return redirect(url_for('listar'))

if __name__ == "__main__":
	app.run(debug=True)