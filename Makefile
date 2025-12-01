YEAR := $(shell date +%Y)
DAY := $(shell date +%d)
IDE := pycharm

create:
	@echo "Setup $(YEAR)-$(DAY)"
	@echo "https://adventofcode.com/$(YEAR)/day/$(DAY)"
	@uv run helpers/download.py $(YEAR) $(DAY)

run:
	@echo "Run $(YEAR)-$(DAY)"
ifeq ($(LEGACY), 1)
	@echo "Legacy mode"
	@cd $(YEAR)/$(DAY) && uv run main.py
else
	@uv run python -m $(YEAR).$(DAY).main
endif

submit:
	@echo "Submit $(YEAR)-$(DAY)"
	@uv run helpers/submit.py $(YEAR) $(DAY) $(ANSWER)
