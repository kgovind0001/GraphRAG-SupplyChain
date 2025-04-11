from pydantic.v1 import BaseModel, Field
from typing import Optional, Dict, List

class SupplierCountInput(BaseModel):
    min_supply_amount: Optional[int] = Field(
        description="Minimum supply amount of the suppliers"
    )
    max_supply_amount: Optional[int] = Field(
        description="Maximum supply amount of the suppliers"
    )
    grouping_key: Optional[str] = Field(
        description="The key to group by the aggregation", 
        enum=["supply_capacity", "location"]
    )

class SupplierListInput(BaseModel):
    sort_by: str = Field(description="How to sort Suppliers by supply capacity", enum=['supply_capacity'])
    k: Optional[int] = Field(description="Number of Suppliers to return")
    description: Optional[str] = Field(description="Description of the Suppliers")
    min_supply_amount: Optional[int] = Field(description="Minimum supply amount of the suppliers")
    max_supply_amount: Optional[int] = Field(description="Maximum supply amount of the suppliers")