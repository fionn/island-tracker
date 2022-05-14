SRC = src/
VENV ?= venv

export PIP_DISABLE_PIP_VERSION_CHECK=1

$(VENV): requirements.txt requirements_dev.txt
	@python -m venv $@ --prompt $@::island
	@source $@/bin/activate && pip install -r $< -r requirements_dev.txt
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
