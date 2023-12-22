from sqlmodel import SQLModel, Field


class PointsSystem(SQLModel, table=True):
    points_id: int | None = Field(default=None, primary_key=True)
    description: str
    points_value: int
