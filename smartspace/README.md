# SmartSpace

Reserva de espaços compartilhados de um condomínio. Python + Flask + MySQL.
Uma única aplicação serve as páginas (Jinja2) e a API JSON (`/api`).

## Instalação no Windows (cmd)

1. Criar e ativar o ambiente virtual:

       python -m venv venv
       venv\Scripts\activate

2. Instalar dependências:

       pip install -r requirements.txt

3. Criar o arquivo `.env` a partir do exemplo e preencher usuário e senha do MySQL:

       copy .env.example .env

4. Criar o banco e as tabelas (cria o banco se não existir, pode ser repetido e também
   corrige acentos gravados errado por versões anteriores):

       python scripts\preparar_banco.py

   Não use `mysql < schema_mysql.sql` pelo prompt do Windows: ele lê o arquivo na
   codificação errada e grava `Salão` como `Sal├úo`. Se preferir o MySQL Workbench,
   abra `database/schema_mysql.sql` nele e execute (raio).

5. Criar o primeiro administrador:

       python scripts\criar_admin.py

6. Iniciar o servidor e abrir http://127.0.0.1:5000

       python run.py

Ao iniciar, o servidor mostra qual usuário, host e banco está usando e testa a conexão.
O `.env` tem prioridade sobre variáveis de ambiente do Windows.

Banco criado antes desta versão: depois do passo 4, ajuste o horário da churrasqueira
(pela tela Gestão > Espaços > Editar, ou pelo SQL abaixo):

    UPDATE smartspace.espaco SET horario_abertura = '08:00', horario_fechamento = '22:00'
    WHERE nome = 'Churrasqueira';

## Telas

| Tela | Rota | Quem |
|------|------|------|
| Login / Cadastro | `/login`, `/cadastro` | visitante |
| Espaços | `/espacos` | logado |
| Reservar (horários e valor) | `/reservar/<id>` | logado |
| Reserva confirmada | `/reserva-confirmada/<id>` | dono da reserva |
| Minhas reservas (cancelar) | `/minhas-reservas` | logado |
| Configurações, Perfil, Sobre | `/configuracoes`, `/perfil`, `/sobre` | logado |
| Gestão de espaços (cadastrar, editar, desativar) | `/admin/espacos` | admin |
| Todas as reservas (filtros, cancelar qualquer) | `/admin/reservas` | admin |

Horários oferecidos: churrasqueira 08:00–15:00, 16:00–22:00 e 08:00–22:00; salão de
festas 08:00–22:00; demais espaços, o horário de funcionamento inteiro. Horários já
ocupados na data aparecem como indisponíveis. O valor (R$ 80,00) é apenas exibido, não
é gravado no banco.

## API JSON

Todas as rotas ficam sob `/api` (por exemplo `POST /api/auth/login`, `GET /api/espacos`,
`POST /api/reservas`). Importar `postman/SmartSpace.postman_collection.json`; o Postman
guarda o cookie de sessão: faça o login e depois chame as demais rotas.

## Testes unitários (não precisam de banco)

    python -m pytest

## Estrutura

    app/models/        Usuario, Admin, Morador, Espaco, Reserva
    app/repositories/  SQL isolado, uma classe por tabela
    app/services/      regras de negócio (auth, espaço, reserva, opções de horário)
    app/routes/        API (auth, espacos, reservas) e páginas (conta, reservas, admin)
    app/templates/     telas Jinja2
    app/static/        CSS, JS, imagens e ícones
    app/utils/         segurança, validadores, decorators, exceções, CSRF, textos
    scripts/           criar_admin.py, preparar_banco.py
