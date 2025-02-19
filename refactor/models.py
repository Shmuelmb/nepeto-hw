from sqlalchemy import (
    Column, DateTime, Float, ForeignKey,
    Integer, JSON, String, func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MarterTrackerProduct(Base):
    __tablename__ = 'MarterTrackerProduct'
    item_id = Column(String, primary_key=True)


class MarterTrackerProductHistory(Base):
    __tablename__ = 'MarterTrackerProductHistory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, default=func.now(), index=True)
    item_id = Column(String, ForeignKey(
        'MarterTrackerProduct.item_id'), index=True)
    review_count = Column(Integer)
    rating = Column(Float)
    offers = Column(String)
    current_seller = Column(JSON)
    current_stock = Column(JSON)
    current_price = Column(JSON)
    current_offers = Column(JSON)
    current_badges = Column(JSON)

    def __str__(self):
        return f'{self.item_id} - {self.date}'
