.DEFAULT_GOAL := build

COLOR_NONE = \033[0m
COLOR_CYAN = \033[36m

help: ## Display this help
	@echo "For more help, run make --help\nOr check the manual: https://www.gnu.org/software/make/manual/html_node/index.html"
	@printf "\nTargets:\n"
	@awk -F ":.*##" '/^[a-zA-Z_-]+:.*?##/ { printf "  ${COLOR_CYAN}%-10s${COLOR_NONE} %s\n", $$1, $$2 }' $(lastword $(MAKEFILE_LIST)) | sort -u
.PHONY: help

build: check test ## (default target) Quick development build: check and test
.PHONY: build

test: ## Quick test with a single Python version
	tox -e py38
.PHONY: test

check: ## Check with pre-commit
	tox -e check
.PHONY: check
