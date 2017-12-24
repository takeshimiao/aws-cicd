TOP_DIR             = $(abspath .)
LIB_DIR            ?= $(TOP_DIR)/build/lib
LIBS                = bottle.py
PYTHON_CMD          = python
ARTIFACTS_DIR      ?= $(TOP_DIR)/dist

.PHONY: all
all: help

.PHONY: help
help: debug
	@echo "Usage: make [ TARGET ... ]";
	@echo "";
	@echo "TARGET:";
	@echo "";
	@echo "  help           - show this help message";
	@echo "  clean          - delete all generated files";
	@echo "  distclean      - delete all generated files and caches";
	@echo "  build          - build the artifacts";
	@echo "  dist           - package the artifacts";
	@echo "  test           - run unit tests";
	@echo "";
	@echo "Default TARGET is 'help'.";

.PHONY: clean
clean:
	python setup.py clean -a

.PHONY: distclean
distclean: clean
	rm -rf $(ARTIFACTS_DIR)
	rm -rf aws_cicd.egg-info

.PHONY: build
build:
	python setup.py build
	bash build.sh $(PYTHON_CMD) $(LIB_DIR) $(LIBS)
	cd lambdas/; make build; cd ..

.PHONY: dist
dist:
	python setup.py sdist
	cp lambdas/dist/* $(ARTIFACTS_DIR)/

.PHONY: test
test:
	python setup.py test
