# SmartSpace — Back-end

Sistema de reserva de espaços compartilhados de um condomínio inteligente.
Projeto acadêmico — ExpoTech 2026.2, categoria ARCHITECTURE (ADS 3º semestre, UniFECAF).

## Stack

- **Linguagem:** Python
- **Framework web:** Flask
- **Banco de dados:** PostgreSQL

## Estrutura de pastas

```
smartspace/
├── app/
│   ├── models/          → entidades de domínio (POO: Usuario, Admin, Morador, Espaco, Reserva)
│   ├── repositories/     → acesso a dados (todo o SQL fica isolado aqui)
│   ├── services/         → regras de negócio (validação, conflito de horário, permissões)
│   ├── routes/            → rotas Flask (endpoints da API)
│   ├── utils/             → segurança (hash de senha), validadores, decorators de permissão
│   ├── config.py          → configurações lidas do .env
│   └── extensions.py      → conexão com o PostgreSQL
├── database/
│   └── schema_postgres.sql  → script DDL para criar o banco
├── tests/
│   └── test_reserva.py    → testes unitários da regra de conflito de horário
├── run.py                 → ponto de entrada da aplicação
├── requirements.txt
└── .env.example
```

### Por que essa organização em camadas?

- **models** conhece só a si mesmo (dados + regrinhas simples de cada entidade)
- **repositories** conhece o banco, mas não sabe de regra de negócio
- **services** conhece as regras de negócio, mas não sabe SQL nem HTTP
- **routes** só traduz HTTP ↔ services

Isso separa responsabilidades (Engenharia de Software) e facilita qualquer
integrante do grupo entender e explicar uma parte isolada do sistema, sem
precisar decorar o projeto inteiro.

## Como rodar

1. Criar e ativar um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate      (Windows)
   source venv/bin/activate   (Mac/Linux)
   ```
2. Instalar as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Copiar `.env.example` para `.env` e preencher com os dados do seu PostgreSQL local.
4. Criar o banco e rodar o schema:
   ```
   createdb smartspace
   psql -d smartspace -f database/schema_postgres.sql
   ```
5. Rodar a aplicação:
   ```
   python run.py
   ```
6. Rodar os testes (não precisa de banco rodando):
   ```
   pytest
   ```

## Estado atual

- [x] Models com herança (Usuario → Admin/Morador) e polimorfismo de permissões
- [x] Repositories (acesso a dados) para as 3 tabelas
- [x] Services com todas as regras de negócio, incluindo conflito de horário
- [x] Rotas Flask funcionais como API JSON (login, cadastro, espaços, reservas)
- [x] Testes unitários da regra de conflito de horário
- [ ] Front-end (telas HTML) — próxima etapa, vai consumir estas mesmas rotas/serviços

## ⚠️ Pontos de atenção do roteiro (não esquecer)

- **Avaliação individual em sala: 09 a 13/11/2026** — qualquer integrante do
  grupo pode ser questionado sobre **qualquer parte** do código, não só a que
  escreveu. Por isso todo arquivo aqui tem docstring explicando o "porquê",
  não só o "o quê".
- **O projeto não pode ser alterado depois da avaliação individual** —
  terminar e testar tudo antes dessa data.
- Ir anotando decisões técnicas e dificuldades ao longo do desenvolvimento
  para facilitar a montagem da documentação final (planejada para perto do prazo).
