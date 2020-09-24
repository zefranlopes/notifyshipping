### API Notificação de Envio com Testes Unitários (Python)

### Repositorio
* https://notifyshipping.herokuapp.com/ 
* https://git.heroku.com/notifyshipping.git

### Ambiente
* Python 3.7
* Heroku
* Postgres

### Frameworks
* Python 3.7
* AioHttp
* SQLAlchemy

### Banco de Dados (*não requer instalação, siga o passo 4.)
* Postgres (ElephantSQL hospedado no Heroku (Free))
* SQlite (Mocar Dados de Testes)


###Documentação Básica
* hhttps://docs.aiohttp.org/en/v3.0.1/
* https://docs.python.org/3/library/unittest.html

###Bibliotecas Utilizada em Teste Unitários 
* API (AioHTTPTestCase)
* Banco de Dados (unittest)


#### 1) Endpoint "/notify" no padrão HTTP/REST/JSON com os métodos:
* GET		200
* PUT		202
* POST		201
* DELETE	204
* ERROR 	500

#### 2) Estrutura da Tabela:

| CAMPO  | TIPO | DESCRICAO |
| --- | --- | --- |
| id | Text | pk |
| ts_updt | TimesTamp | Data/Hora do Registro |
| ts_send | TimesTamp | Data/Hora do Agendamento |
| ts_recv | TimesTamp | Data/Hora da Confirmação  |
| remittee | Text | Destinatário da Notificação |
| status | Text | Status da Notificação |
| payload | JSON | Mensagem da Notificação |


#### 3) Estrutura da Tabela:

	|ws
	|db
	|model
	|controller
	|exceptions 
	|tests

	```bash
	ws - arquivo webservice da aplicacao
	```
	```bash
	db - arquivo conexão com banco de dados (server / mock)
	```
	```bash
	model - arquivo estrutura des tabelas
	```
	```bash
	controller - arquivo para realizar as regras de negocios (ws -> controller -> model)
	```
	```bash
	exceptions - arquivo exceptions customizadas 
	```
	```bash
	tests - arquivo coleciona uma suite de tetes da API e Banco de Dados
	```

#### 4) Rodar Aplicação e Testes (LOCAL):
* py3 ws.py
	- roda o webservice 

* py3 tests.py
	- roda os testes unitarios 
	
#### 5) Ambiente Deploy Free Heroku (WEB) ***opcional por se tratar de conteúdo apenas academico
* Utilizado passo a passo para montar seu ambiente virtual "Python"
* https://devcenter.heroku.com/articles/getting-started-with-python#prepare-the-app

