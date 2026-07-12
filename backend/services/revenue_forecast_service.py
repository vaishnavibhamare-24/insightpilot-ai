from functools import lru_cache
from typing import Any

from ml.forecasting.predict import RevenueForecaster


@lru_cache
def get_revenue_forecaster() -> RevenueForecaster:
    return RevenueForecaster()


class RevenueForecastService:
    def forecast(
        self,
        months: int,
    ) -> dict[str, Any]:
        forecaster = get_revenue_forecaster()

        return forecaster.forecast(months)