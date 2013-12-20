.PHONY: flakes tests clean

all: flakes

flakes:
	pyflakes tests setup.py

test_venv: requirements.txt
	rm -rf test_venv
	virtualenv test_venv
	bash -c 'source test_venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install -e .'

tests: flakes test_venv
	bash -c "source test_venv/bin/activate && testify tests"

test_signup: flakes test_venv
	bash -c "source test_venv/bin/activate && testify tests.test_signup"

test_rosi: flakes test_venv
	bash -c "source test_venv/bin/activate && testify tests.test_rosi_login"

serve_signup: flakes test_venv
	bash -c "source test_venv/bin/activate && python selenium_examples/signup.py"

serve: flakes test_venv
	bash -c "source test_venv/bin/activate && python selenium_examples/set_user_name.py"

start_selenium:
	bash -c "java -jar bin/selenium-server-standalone-2.35.0.jar \
		-Dwebdriver.chrome.driver=bin/chromedriver"

create_fixtures: test_venv
	bash -c "source test_venv/bin/activate && python create_fixtures.py"

delete_fixtures:
	if [ -a example.db ] ; \
	then \
		rm example.db  ; \
	fi;

clean: delete_fixtures
	rm -rf test_venv
	find . -iname '*.pyc' -delete

