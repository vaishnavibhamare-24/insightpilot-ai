from pydantic import BaseModel, Field


class ChurnPredictionRequest(BaseModel):
    total_orders: int = Field(ge=0)
    lifetime_revenue: float = Field(ge=0)
    average_order_value: float = Field(ge=0)
    days_since_last_order: int = Field(ge=0)
    customer_lifetime_days: int = Field(ge=0)
    purchase_frequency: float = Field(ge=0)
    estimated_clv: float = Field(ge=0)


class ChurnPredictionResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    risk_level: str


class RevenueForecastItem(BaseModel):
    month: str
    predicted_revenue: float


class RevenueForecastResponse(BaseModel):
    forecast_horizon: int
    model_name: str
    predictions: list[RevenueForecastItem]