SRC_DIR := app/src

.PHONY: formatters lint type-check
formatters:
	@echo "Запуск форматирования кода..."
	cd $(SRC_DIR) && isort . && black --line-length 78 .

lint:
	@echo "Запуск линтера..."
	cd $(SRC_DIR) && flake8 .

type-check:
	@echo "Проверка типов с mypy..."
	export MYPYPATH=app/src && mypy --ignore-missing-imports app/src

check: formatters lint type-check
	@echo "Все проверки завершены."



