import pytest
import app as modulo


@pytest.fixture
def client():
    # Cada teste começa com a lista de demonstração em estado conhecido.
    modulo.alunos.clear()
    modulo.alunos.append({
        "id": 1,
        "nome": "Ana Souza",
        "telefone": "(51) 900000001",
        "data_cadastro": "2026-10-16",
        "periodo": "10/2026",
        "vencimento": "2026-10-20",
        "valor": 100.00,
        "status": "Pendente",
    })
    modulo.app.config.update(TESTING=True, SECRET_KEY="chave-de-teste")
    with modulo.app.test_client() as test_client:
        yield test_client
    modulo.alunos.clear()


def test_telas_principais_carregam(client):
    assert client.get("/").status_code == 200
    assert client.get("/cadastro").status_code == 200
    assert client.get("/resultados").status_code == 200


def test_cadastro_sem_nome_e_rejeitado(client):
    resposta = client.post("/cadastro", data={
        "nome": "",
        "data_cadastro": "2026-10-17",
        "periodo": "11/2026",
        "vencimento": "2026-11-10",
    })
    assert resposta.status_code == 200
    assert len(modulo.alunos) == 1
    assert "obrigatórios" in resposta.get_data(as_text=True)


def test_cadastro_com_dados_validos_adiciona_aluno(client):
    resposta = client.post("/cadastro", data={
        "nome": "Bruno Lima",
        "telefone": "(51) 90000-0001",
        "data_cadastro": "2026-10-17",
        "periodo": "11/2026",
        "vencimento": "2026-11-10",
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert any(a["nome"] == "Bruno Lima" for a in modulo.alunos)
    assert "sucesso" in resposta.get_data(as_text=True).lower()


def test_cadastro_duplicado_no_mes_e_rejeitado(client):
    resposta = client.post("/cadastro", data={
        "nome": "Ana Souza",
        "telefone": "",
        "data_cadastro": "2026-10-17",
        "periodo": "10/2026",
        "vencimento": "2026-10-25",
    })
    assert resposta.status_code == 200
    assert len(modulo.alunos) == 1
    assert "Já existe" in resposta.get_data(as_text=True)


def test_exclusao_remove_registro(client):
    resposta = client.post("/aluno/1/excluir", follow_redirects=True)
    assert resposta.status_code == 200
    assert modulo.alunos == []
    assert "excluído com sucesso" in resposta.get_data(as_text=True)


def test_exclusao_de_id_inexistente_nao_quebra_a_aplicacao(client):
    resposta = client.post("/aluno/999/excluir", follow_redirects=True)
    assert resposta.status_code == 200
    assert len(modulo.alunos) == 1
    assert "não foi encontrado" in resposta.get_data(as_text=True)
