# CMO - Compilazione Moduli Online

## Istruzioni per installare ed eseguire il progetto:

1. Scaricare e scompattare il pacchetto

2. Aprire il progetto "tesina" con PyCharm

3. File->Settings...->Project: tesina->Project Interpreter->simbolo ingranaggio->Add...->Existing environment->OK

4. Run->Edit configurations...->Python interpreter:->selezionare quello aggiunto nel passaggio precedente->OK

In alternativa è possibile cancellare il venv presente, crearne uno nuovo nella posizione desiderata ed eseguire il comando:

	pip install -r requirements.txt
	
per installare i pacchetti necessari all'esecuzione del progetto.



## Impostazioni per il database:

1. I database supportati sono i seguenti:

	Microsoft SQL Server 2008/2008R2, 2012, 2014, 2016, 2017 e Azure SQL Database

2. All'interno del file "/tesina/tesina/settings.py", nella sezione:
	
	```
	DATABASES = {
		'default': {
			'ENGINE': 'sql_server.pyodbc',
			'NAME': 'djangodb',
			'HOST': 'OMEN-LOLLO\SQLEXPRESS',
			'PORT': '',
			'USER': 'djangoadmin',
			'PASSWORD': 'djangopw',
		}
	}
	```

	sostituire a 'OMEN-LOLLO\SQLEXPRESS' il nome della propria istanza di SQL Server
	
3. In SQL Server creare un utente 'djangoadmin':
	- istanza di SQL Server->Sicurezza->Account di accesso->tasto destro->Nuovo account di accesso...
		- Nome account di accesso: ->inserire 'djangoadmin'
		- Autenticazione SQL Server
			- Password:->inserire 'djangopw'
			- Conferma password:->inserire 'djangopw'
			- Applica criteri password->togliere la spunta
		- Ruoli del server->sysadmin->Ok
		
4. In SQL Server creare un database 'djangodb':
	- istanza di SQL Server->Database->tasto destro->Nuovo database...
		- Nome database:->inserire 'djangodb'
		- Proprietario:->inserire 'djangoadmin'->Ok

5. Con django manage.py eseguire:
	
	```
	makemigration form
	```
	
	```
	sqlmigrate form 0001
	```
	
	```
	migrate
	```

In alternativa è possibile utilizzare nomi differenti da quelli indicati, ma devono essere sostituiti anche nella sezione indicata nel punto 2.

**In caso di errori provare le seguenti soluzioni:**
- avviare SQL Server come amministratore
- in SQL Server: istanza di SQL Server->tasto destro->Proprietà->Sicurezza->Autenticazione di SQL Server e di Windows->Ok
- da SQL Server Configuration Manager (C:\Windows\SysWOW64\SQLServerManager11.msc nel caso di SQL Server 2012) controllare che per ogni configurazione siano attivati i protocolli Named Pipes e TCP/IP.
	
**È poi possibile utilizzare il database di esempio invece di crearne uno nuovo utilizzando 'djangodb.bacpac':**
- istanza di SQL Server->Database->tasto destro->Importa applicazione livello dati...->Avanti->Importa da disco locale->Sfoglia...->selezionare il file djangodb.bacpac->Avanti->Avanti->Fine->al termine dell'operazione->Chiudi
