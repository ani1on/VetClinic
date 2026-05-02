from pydantic import Field
from typing import Any, Dict, List
from . import ORMModel

class DashboardMetricsResponse(ORMModel):
    total_appointments: int
    appointments_this_week: int
    pending_appointments: int
    total_users: int
    new_users_this_week: int
    total_products: int
    low_stock_products: int
    pending_reviews: int

class AppointmentsStatsResponse(ORMModel):
    total: int
    by_status: List[Dict[str, Any]]   # [{status: "pending", count: 5}, ...]