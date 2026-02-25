PYTHON ?= venv/bin/python

.PHONY: runbooks index test run eval clean all

runbooks:
	cd src && $(PYTHON) generate_runbooks.py

index:
	cd src && $(PYTHON) index_runbooks.py

test:
	$(PYTHON) -m pytest tests/ -v -m "not ollama"

run:
	cd src && $(PYTHON) -m streamlit run dashboard.py

eval:
	cd src && $(PYTHON) generate_eval_questions.py
	cd src && $(PYTHON) evaluate_retrieval.py

clean:
	rm -rf runbooks/ data/

all: runbooks index test
