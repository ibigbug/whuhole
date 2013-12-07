.PHONY: components stylus

tpls = $(shell find templates -name '*.html')

build: components stylus tpl
	@component build -o ../whuhole/static -n app -p .

components: component.json
	@component install 

stylus:
	stylus index.styl -I stylus 

tpl:
	$(foreach t, $(tpls), component-convert $(t);)

clean:
	@rm -fr components
	@rm -fr templates/*.js

pyfiles = $(shell find ./whuhole -name '*.py' ! -path '*__init__.py')

lint:
	@flake8 $(pyfiles)
