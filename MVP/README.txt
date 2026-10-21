PROTÓTIPO — GESTÃO DE ACADEMIA

O que é:
Protótipo acadêmico local com três telas próprias:
1. Entrada principal (/)
2. Cadastro de aluno e mensalidade (/cadastro)
3. Listagem de alunos e mensalidades (/resultados), com opção de excluir um cadastro demonstrativo após confirmação.

IMPORTANTE:
- Use apenas dados fictícios.
- Os registros ficam apenas na memória enquanto o servidor está ligado; ao reiniciar a aplicação, voltam aos dados iniciais.
- A exclusão remove o registro selecionado da lista em memória após uma confirmação. Não existe lixeira de recuperação nem persistência em banco de dados.
- Este protótipo NÃO é um sistema pronto para uso real, não possui banco de dados,
  autenticação real ou persistência. Não insira dados pessoais verdadeiros.
- A chave Flask do app.py é apenas para demonstração local.

COMO EXECUTAR NO WINDOWS:
1. Instale Python 3.12 ou versão compatível.
2. Extraia a pasta do ZIP.
3. Abra a pasta gestao_academia_prototipo no Visual Studio Code.
4. No VS Code, escolha Terminal > Novo Terminal.
5. Execute:
   python -m venv .venv
6. Ative o ambiente:
   PowerShell: .\.venv\Scripts\Activate.ps1
   Prompt de Comando: .venv\Scripts\activate.bat
7. Instale a dependência:
   pip install -r requirements.txt
8. Inicie:
   python app.py
9. Abra no navegador:
   http://127.0.0.1:5000

COMO CAPTURAR AS EVIDÊNCIAS:
- Tela 1: abra http://127.0.0.1:5000/
- Tela 2: clique em “Cadastrar aluno e mensalidade”.
- Tela 3: clique em “Alunos e mensalidades” ou salve um cadastro fictício.
- Maximize o navegador e ajuste o zoom para que a tela inteira fique legível.
- Capture cada tela separadamente com Win + Shift + S.
- Recorte para mostrar apenas a interface, sem barra de tarefas ou áreas desnecessárias.
- Confira se todos os textos estão nítidos antes de inserir na atividade.

Este protótipo não substitui validação com o representante real da Academia Jump.


FUNCIONALIDADES DO MVP
- Tela inicial com navegação para cadastro e consulta.
- Cadastro demonstrativo com nome, telefone opcional, data de cadastro, período de referência e vencimento.
- Valor mensal fixo de R$ 100,00 no protótipo.
- Consulta dos registros demonstrativos de alunos e mensalidades.
- Exclusão de um registro selecionado mediante confirmação.

ARQUITETURA E LIMITAÇÕES
A aplicação é um protótipo web em Flask com templates Jinja2 e estilos CSS. Os dados são mantidos em uma lista Python em memória; não há banco de dados, autenticação, controle de acesso ou persistência entre reinicializações. Use somente dados fictícios. A exclusão é definitiva dentro da sessão em execução e não existe mecanismo de recuperação.

VALIDAÇÕES
O servidor verifica campos obrigatórios, formato do período de referência e consistência básica das datas antes de adicionar um registro. Essas validações demonstrativas não substituem os controles necessários em uma aplicação de produção.
