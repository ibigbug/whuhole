
build: components index.js stylus
	@component build -o ../whuhole/static/ -n whuhole -p .

stylus:
	@stylus -I ./styles whuhole.styl

components: component.json
	@component install --dev

clean:
	rm -fr build components

.PHONY: clean
