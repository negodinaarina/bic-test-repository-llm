import csv
from datetime import datetime
from typing import Optional

from src.config import BENCHMARKS_DIR


def save_benchmark_results(
    model: str, results: list[tuple[str, str, int, float, Optional[str]]]
) -> str:
    """
    Сохраняет результаты бенчмарка в CSV-файл.
    :param results: список кортежей (prompt, run, latency, error)
    :param model: название модели
    :return: путь к созданному файлу
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_results_{model.replace('/', '_')}_{timestamp}.csv"
    filepath = BENCHMARKS_DIR / filename

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["model", "prompt", "run", "latency_seconds", "error"]
        )
        for model, prompt, run, latency, error in results:
            writer.writerow(
                [model, prompt, run, f"{latency:.4f}", error or ""]
            )

    return filepath
