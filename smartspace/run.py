"""
Ponto de entrada da aplicação.

Rode com: python run.py
(depois de configurar o .env e instalar as dependências — ver README.md)
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
