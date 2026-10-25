from datetime import date
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
# Em ambiente local, usa uma chave de demonstração. Defina FLASK_SECRET_KEY
# por variável de ambiente fora dos testes e nunca reutilize a chave de exemplo.
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "chave-local-apenas-para-prototipo"
)
app.config["TESTING"] = os.environ.get("FLASK_TESTING", "0") == "1"

# Dados fictícios mantidos apenas na memória enquanto o servidor estiver ligado.
alunos = [
    {
        "id": 1,
        "nome": "Ana Souza",
        "telefone": "(51) 90000-0000",
        "data_cadastro": "16/10/2026",
        "periodo": "10/2026",
        "vencimento": "20/10/2026",
        "valor": 100.00,
        "status": "Pendente",
    }
]

@app.template_filter("data_br")
def data_br(valor):
    """Converte a data para o padrão brasileiro."""
    from datetime import date

    try:
        return date.fromisoformat(valor).strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return valor
    
@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        data_cadastro = request.form.get("data_cadastro", "").strip()
        periodo = request.form.get("periodo", "").strip()
        vencimento = request.form.get("vencimento", "").strip()

        if not nome or not data_cadastro or not periodo or not vencimento:
            flash("Preencha todos os campos obrigatórios indicados com *.", "erro")
            return render_template("cadastro.html", valores=request.form)

        

        if telefone and not re.fullmatch(
            r"(?:\([0-9]{2}\) ?9[0-9]{8}|[0-9]{11})",
            telefone
        ):
            flash(
                "Informe o telefone com DDD e 9 dígitos. Ex.: (21)9XXXXXXXX ou 219XXXXXX.",
                "erro"
            )
            return render_template("cadastro.html", valores=request.form)


        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", periodo):
            flash("Informe o período no formato MM/AAAA, por exemplo 11/2026.", "erro")
            return render_template("cadastro.html", valores=request.form)

        try:
            data_cadastro_obj = date.fromisoformat(data_cadastro)
            vencimento_obj = date.fromisoformat(vencimento)
        except ValueError:
            flash("Informe datas válidas para o cadastro e o vencimento.", "erro")
            return render_template("cadastro.html", valores=request.form)

        if vencimento_obj < data_cadastro_obj:
            flash("A data de vencimento não pode ser anterior à data de cadastro.", "erro")
            return render_template("cadastro.html", valores=request.form)

        duplicado = any(
            a["nome"].casefold() == nome.casefold() and a["periodo"] == periodo
            for a in alunos
        )
        if duplicado:
            flash("Já existe um cadastro de demonstração com esse nome e período. Use outro dado fictício.", "erro")
            return render_template("cadastro.html", valores=request.form)

        # Protótipo demonstrativo: não grava em banco de dados.
        novo_id = max((a["id"] for a in alunos), default=0) + 1
        alunos.insert(0, {
            "id": novo_id,
            "nome": nome,
            "telefone": telefone or "Não informado",
            "data_cadastro": data_cadastro,
            "periodo": periodo,
            "vencimento": vencimento,
            "valor": 100.00,
            "status": "Pendente",
        })
        flash("Cadastro demonstrativo realizado com sucesso.", "sucesso")
        return redirect(url_for("resultados"))

    return render_template("cadastro.html", valores={})

@app.route("/resultados")
def resultados():
    hoje = date.today()

    for aluno in alunos:
        if aluno.get("status") == "Paga":
            continue

        try:
            vencimento = date.fromisoformat(aluno["vencimento"])
        except (ValueError, TypeError):
            try:
                from datetime import datetime
                vencimento = datetime.strptime(
                    aluno["vencimento"], "%d/%m/%Y"
                ).date()
            except (ValueError, TypeError):
                aluno["status"] = "Pendente"
                continue

        aluno["status"] = (
            "Atrasada" if vencimento < hoje else "Pendente"
        )

    return render_template("resultados.html", alunos=alunos)

@app.route("/aluno/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    aluno = next((a for a in alunos if a["id"] == aluno_id), None)
    if aluno is None:
        flash("O aluno não foi encontrado. A lista pode ter sido atualizada.", "erro")
    else:
        alunos.remove(aluno)
        flash(f"Cadastro demonstrativo de {aluno['nome']} excluído com sucesso.", "sucesso")
    return redirect(url_for("resultados"))

if __name__ == "__main__":
    # O modo de depuração fica desativado por padrão.
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
