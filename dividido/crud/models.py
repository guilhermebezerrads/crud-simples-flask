from crud import db

class Tarefa(db.Model):

	__tablename__ = 'tarefas'

	id = db.Column(db.Integer, primary_key=True)
	titulo = db.Column(db.String, nullable=False)

	def __init__(self, titulo):
		self.titulo = titulo
