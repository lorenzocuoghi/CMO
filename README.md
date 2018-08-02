# CMO - Compilazione Moduli Online

Istruzioni per installare ed eseguire il progetto:
-Scaricare e scompattare il pacchetto
-Apripre il progetto "tesina" con PyCharm
-File->Settings...->Project: tesina->Project Interpreter
	simbolo ingranaggio->Add...->Existing environment->OK
-Run->Edit configurations...->Python interpreter:
	selezionare quello aggiunto nel passaggio precedente
	->OK

In alternativa è possibile cancellare il venv presente, crearne uno nuovo nella posizione desiderata ed eseguire il comando:
	pip install -r requirements.txt
per installare i pacchetti necessari all'esecuzione del progetto.
