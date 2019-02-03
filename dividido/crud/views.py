from flask import render_template, url_for, redirect, request
from crud import app, db, forms, models

@app.route('/criar', methods=['POST', 'GET'])
def criar():
	form = forms.CriarForm()

	if form.validate_on_submit():
		nova_tarefa = models.Tarefa(form.titulo.data)
		db.session.add(nova_tarefa)
		db.session.commit()

		return redirect(url_for('listar'))

	return render_template('criar.html', form=form)

@app.route('/')
@app.route('/listar')
def listar():

	tarefas = models.Tarefa.query.all()

	return render_template('listar.html', tarefas=tarefas)


@app.route('/atualizar/<id>', methods=['POST', 'GET'])
def atualizar(id):
	form = forms.AtualizarForm()

	tarefa = models.Tarefa.query.filter_by(id=id).first_or_404()

	if form.validate_on_submit():
		tarefa.titulo = form.titulo.data
		db.session.commit()

		return redirect(url_for('listar'))
	elif request.method == 'GET':
		form.titulo.data = tarefa.titulo

	return render_template('atualizar.html', form=form)


@app.route('/excluir/<id>', methods=['GET'])
def excluir(id):

	tarefa = models.Tarefa.query.filter_by(id=id).first_or_404()

	db.session.delete(tarefa)
	db.session.commit()

	return redirect(url_for('listar'))