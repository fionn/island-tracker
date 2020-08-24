SRC = src/
VENV ?= venv

$(VENV): requirements.txt
	@python -m venv $@ --prompt $@::island
	@source $@/bin/activate && pip --disable-pip-version-check install -r $<
	@echo "Enter virtual environment: source venv/bin/activate"

tags: $(SRC)
	@ctags --languages=python --python-kinds=-i -R $(SRC)

.PHONY: outdated
outdated:
	@source $(VENV)/bin/activate && pip list --outdated

.PHONY: lint
lint:
	@pylint -f colorized $(SRC)

.PHONY: typecheck
typecheck:
	@mypy $(SRC)
