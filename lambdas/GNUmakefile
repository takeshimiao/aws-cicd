TOP_DIR             = $(abspath .)
ARTIFACTS_DIR      ?= $(TOP_DIR)/dist
DST_LIB_DIR        ?= $(TOP_DIR)/lib
SRC_LIB_DIR        ?= $(TOP_DIR)/../build/lib
VERSION				= $(shell egrep version ../setup.py | cut -d "'" -f 2)

.PHONY: all
all: help

.PHONY: help
help:
	@echo "Usage: make [ TARGET ... ]";
	@echo "";
	@echo "TARGET:";
	@echo "";
	@echo "  help           - show this help message";
	@echo "  clean          - delete all generated files";
	@echo "  distclean      - delete all generated files and caches";
	@echo "  build          - build the artifacts";
	@echo "";
	@echo "Default TARGET is 'help'.";

.PHONY: clean
clean:
	rm -rf $(DST_LIB_DIR)

.PHONY: distclean
distclean: clean
	rm -rf $(ARTIFACTS_DIR)

.PHONY: build
build:
	bash build.sh $(SRC_LIB_DIR) $(DST_LIB_DIR) $(ARTIFACTS_DIR) $(VERSION)
