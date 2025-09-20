YEAR := $(shell date +%Y)
DAY := $(shell date +%d)
IDE := pycharm

create:
	@echo "Setup $(YEAR)-$(DAY)"
	@uv run helpers/download.py $(YEAR) $(DAY) && $(IDE) $(YEAR)/$(DAY)/main.py

run:
	@echo "Run $(YEAR)-$(DAY)"
	@cd $(YEAR)/$(DAY) && uv run main.py
