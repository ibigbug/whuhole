run:
	@python manager.py runserver

#translate
babel-extract:
	@python setup.py extract_messages -o messages.pot

language = zh
i18n = whuhole/translations
babel-init: babel-extract
	@python setup.py init_catalog -i messages.pot -d ${i18n} -l ${language}

babel-compile:
	@python setup.py compile_catalog -d ${i18n}

babel-update: babel-extract
	@python setup.py update_catalog -i messages.pot -d ${i18n}

py_files := $(shell find whuhole -name '*.py' ! -path '*__init__.py')
lint:
	@flake8 $(py_files)
