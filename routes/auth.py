from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash

from database import db
from models.usuario import Usuario

auth = Blueprint("auth", __name__)

@auth.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email","").strip().lower()
        senha = request.form.get("senha","")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "erro")
            return redirect("/cadastro")

        usuario_existente = Usuario.query.filter_by(
            email=email
        ).first()

        if usuario_existente:
            flash("Este e-mail já está cadastrado.", "erro")
            return redirect("/cadastro")

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha_hash
        )

        db.session.add(novo_usuario)
        db.session.commit()

        flash("Cadastro realizado com sucesso!", "sucesso")
        return redirect("/cadastro")

    return render_template("cadastro.html")
