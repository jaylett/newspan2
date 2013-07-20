.PHONY: css

css: static/css/*.css

static/css/base.css: $(wildcard sass/*.scss)
	sassc sass/base.scss > static/css/base.css
