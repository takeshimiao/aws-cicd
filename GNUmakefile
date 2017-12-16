TOP_DIR             = $(abspath .)
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

.PHONY: dist
dist:
	python setup.py sdist

.PHONY: test
test:
	python setup.py test
