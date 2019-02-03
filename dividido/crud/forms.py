from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CriarForm(FlaskForm):

    titulo = StringField("Título da tarefa", validators=[DataRequired()])
    submit = SubmitField("Criar")

class AtualizarForm(FlaskForm):

    titulo = StringField("Título da tarefa", validators=[DataRequired()])
    submit = SubmitField("Atualizar")