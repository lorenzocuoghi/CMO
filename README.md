# CMO - Compilazione Moduli Online

Istruzioni per installare ed eseguire il progetto:

1. Scaricare e scompattare il pacchetto

2. Apripre il progetto "tesina" con PyCharm

3. File->Settings...->Project: tesina->Project Interpreter->simbolo ingranaggio->Add...->Existing environment->OK

4. Run->Edit configurations...->Python interpreter:->selezionare quello aggiunto nel passaggio precedente
	->OK

In alternativa è possibile cancellare il venv presente, crearne uno nuovo nella posizione desiderata ed eseguire il comando:

	pip install -r requirements.txt
per installare i pacchetti necessari all'esecuzione del progetto.
