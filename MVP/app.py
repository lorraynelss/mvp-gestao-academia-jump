from datetime import date
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave-local-apenas-para-prototipo"

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
    app.run(debug=True)
