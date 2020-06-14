init:
	pip install -r requirements.txt

test:
	coverage run -m unittest tests/test*.py

run-watcher-once:
	python watcher.py

run-watcher:
	python watcher.py --interval 60

run-recorder:
	python recorder.py

test-report:
	coverage report

.PHONY: init test test-report run-watcher run-watcher-once run-recorder
