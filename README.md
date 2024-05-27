📚 BiblioTECH

Sobre o Projeto
BiblioTECH é um sistema de gerenciamento de bibliotecas desenvolvido como parte da cadeira de Modelagem e Projeto de Banco de Dados. Nosso objetivo é facilitar o controle de empréstimos, catalogação de livros e gestão de usuários, proporcionando uma interface intuitiva e eficiente.

Equipe de Desenvolvimento
Thiago Costa Queiroz
Vinicius Cahu
Matheus Veloso
Funcionalidades Principais
📖 Gerenciamento de Livros: Cadastro, edição e exclusão de livros.
👤 Gerenciamento de Usuários: Controle de membros da biblioteca.
📅 Controle de Empréstimos: Empréstimo e devolução de livros com histórico detalhado.
🔍 Busca Avançada: Ferramenta de busca eficiente por título, autor ou categoria.
📊 Relatórios: Geração de relatórios sobre o acervo e os empréstimos.
Tecnologias Utilizadas
Linguagem de Programação: Python
Framework de Interface: Streamlit
Banco de Dados: SQL
Estrutura do Projeto
bash
Copiar código
BiblioTECH/
├── app/
│   ├── pages/            # Páginas da aplicação
│   ├── services/         # Lógica de negócio
│   ├── database/         # Configurações e modelos do banco de dados
│   └── static/           # Arquivos estáticos (CSS, imagens)
├── .env                  # Variáveis de ambiente
├── README.md             # Documentação do projeto
└── requirements.txt      # Dependências do projeto
Instalação e Configuração
Clone o repositório:
bash
Copiar código
git clone https://github.com/seu-usuario/BiblioTECH.git
Navegue até o diretório do projeto:
bash
Copiar código
cd BiblioTECH
Crie um ambiente virtual:
bash
Copiar código
python -m venv venv
Ative o ambiente virtual:
bash
Copiar código
# No Windows
venv\Scripts\activate

# No MacOS/Linux
source venv/bin/activate
Instale as dependências:
bash
Copiar código
pip install -r requirements.txt
Configure as variáveis de ambiente no arquivo .env:
env
Copiar código
DB_HOST=localhost
DB_USER=seu-usuario
DB_PASS=sua-senha
DB_NAME=bibliotech
Inicie a aplicação:
bash
Copiar código
streamlit run app/main.py
Uso
Acesse o sistema em http://localhost:8501.
Navegue pelo painel administrativo para gerenciar livros, usuários e empréstimos.
Contribuição
Contribuições são bem-vindas! Para contribuir, siga os passos abaixo:

Faça um fork do projeto.
Crie uma nova branch com sua funcionalidade ou correção:
bash
Copiar código
git checkout -b minha-nova-funcionalidade
Commit suas mudanças:
bash
Copiar código
git commit -m 'Adiciona nova funcionalidade'
Envie para o branch principal:
bash
Copiar código
git push origin minha-nova-funcionalidade
Abra um Pull Request.
