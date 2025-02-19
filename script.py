from sqlalchemy import (
    Column, DateTime, Float, ForeignKey, Integer, JSON, String, func
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import requests
import json
Base = declarative_base()


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
    """ JSON Structure:
    # seller_id = Column(String)
    # seller_display_name = Column(String)
    # seller_avg_rating = Column(Float)
    # seller_review_count = Column(Integer)
    # seller_wfs_enabled = Column(Boolean, default=False)
    """

    current_stock = Column(JSON)
    """ JSON Structure:
    # stock = Column(Integer, nullable=False, default=0)
    # stock_wfs = Column(Integer, default=0)
    # stock_sf = Column(Integer, default=0)
    # stock_walmart = Column(Integer, default=0)
    """

    current_price = Column(JSON)
    """ JSON Structure:
    # price = Column(Float, nullable=False)
    # price_lowest = Column(Float)
    # price_walmart = Column(Float)
    # price_lowest_wfs = Column(Float)
    # price_lowest_sf = Column(Float)
    """

    current_offers = Column(JSON)
    """ JSON Structure:
    # offer_count = Column(Integer)
    # offer_count_wfs_sellers = Column(Integer)
    # offer_count_sf_sellers = Column(Integer)
    """

    current_badges = Column(JSON)
    """ JSON Structure:
    # badge_best_seller = Column(Boolean, default=False)
    # badge_popular_pick = Column(Boolean, default=False)
    # badge_x_amount_sold = Column(Integer)
    # badge_x_amount_in_cart = Column(Integer)
    """

    def __str__(self):
        return f'{self.item_id} - {self.date}'


class MarterTrackerProduct(Base):
    __tablename__ = 'MarterTrackerProduct'
    item_id = Column(String, primary_key=True)


def create_history_records(response_data, item_id):
    history_records = []

    price_history = response_data.get('result')[0].get(
        'stats').get('low_price_history', [])

    for price_point in price_history:
        price = price_point.get('price', -1)
        history_record = MarterTrackerProductHistory(
            item_id=item_id,
            date=datetime.fromtimestamp(price_point.get('timestamp', 0)),
            review_count=-1,
            rating=-1,
            offers="",
            current_seller={},
            current_stock={},
            current_price={
                "price": price,
                "price_lowest": price,
                "price_walmart": -1,
                "price_lowest_wfs": -1,
                "price_lowest_sf": -1
            },
            current_offers={
                "offer_count": -1,
                "offer_count_wfs_sellers": -1,
                "offer_count_sf_sellers": -1
            },
            current_badges={
                "badge_best_seller": False,
                "badge_popular_pick": False,
                "badge_x_amount_sold": -1,
                "badge_x_amount_in_cart": -1
            }
        )
        history_records.append(history_record)

    return history_records


ids = ['46480251 ', '1', '2', '3', '4', '5', '6', '7', '8', '9']
engine = create_engine(
    'postgresql://root:1234@db:5432/test', echo=False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
for id in ids:
    try:
        with Session() as session:
            product = MarterTrackerProduct(item_id=id.strip())
            session.add(product)
            session.commit()
    except Exception:
        print(f'{id.strip()} already exists')


params = {'low_price_history': 1, 'stats': 1000}
headers = {'api-key': '717d12a2ffbfa6752e91ae36f9687284'}
for id in ids:
    url = f'https://dataspark.co/api/v1/product/{id}'
    res = requests.get(url, params=params, headers=headers)
    response = json.loads(res.text)
    history_records = create_history_records(response, id)
    for record in history_records:
        try:
            with Session() as session:
                session.add(record)
                session.commit()
        except Exception:
            print(f'This record for {record.item_id} already exists')
