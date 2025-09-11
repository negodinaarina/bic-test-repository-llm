from pydantic import BaseModel


class BenchmarkStatisticsSchema(BaseModel):
    model: str
    avg: float | None
    min: float | None
    max: float | None
    std_dev: float | None
    total_runs: int
    failed_runs: int
