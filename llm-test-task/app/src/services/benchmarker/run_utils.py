import asyncio
import statistics
import time
from typing import Optional

from src.config import settings
from src.logger import logger
from src.schemas.benchmarks import BenchmarkStatisticsSchema
from src.schemas.prompts import PromptRequestSchema
from src.services.benchmarker.file_utils import save_benchmark_results
from src.services.openrouter.client import open_router_client


async def _run_single_prompt(
    prompt: str,
    model: str,
    run: int,
    semaphore: asyncio.Semaphore,
    max_tokens: int = settings.MAX_TOKENS,
) -> tuple[str, str, int, float, Optional[str]]:
    """
    Один прогон генерации для конкретного промпта.
    :param prompt: входящий промпт
    :param model: модель для генерации
    :param run: номер генерации
    :param semaphore: семафор для ограничения количества
    парралельных выполнений
    :param max_tokens: максимальное количество токенов
    """
    async with semaphore:
        start = time.perf_counter()
        try:
            logger.info(
                f"STARTED SINGLE PROMPT IN BENCHMARK "
                f"MODEL: {model}, RUN: {run}"
            )
            await open_router_client.post_prompt(
                request=PromptRequestSchema(prompt=prompt, model=model),
                max_tokens=max_tokens,
            )
            latency = time.perf_counter() - start
            return model, prompt, run, latency, None
        except Exception as e:
            logger.error(str(e.__dict__))
            latency = time.perf_counter() - start
            return model, prompt, run, latency, str(e)


async def run_benchmark(
    prompts: list[str],
    model: str,
    runs: int = 5,
    concurrency: int = 5,
    max_tokens: int = settings.MAX_TOKENS,
) -> BenchmarkStatisticsSchema:
    """
    Запускает бенчмарк: несколько прогонов для набора промптов.
    Возвращает метрики.
    :param prompts: список строк-промптов для генерации
    :param model: модель для генерации
    :param runs: количество генераций промта
    :param concurrency: ограничение на количество параллельно
    исполняемых генераций
    :param max_tokens: максимальное количество токенов
    """
    semaphore = asyncio.Semaphore(concurrency)

    tasks = [
        _run_single_prompt(prompt, model, run, semaphore, max_tokens)
        for prompt in prompts
        for run in range(1, runs + 1)
    ]

    results = await asyncio.gather(*tasks)

    save_benchmark_results(model, results)

    latencies = [
        latency
        for model, prompt, _, latency, error in results
        if error is None
    ]

    metrics = {
        "model": model,
        "avg": statistics.mean(latencies) if latencies else None,
        "min": min(latencies) if latencies else None,
        "max": max(latencies) if latencies else None,
        "std_dev": statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
        "total_runs": len(results),
        "failed_runs": sum(
            1 for _, _, _, _, error in results if error is not None
        ),
    }

    return metrics
