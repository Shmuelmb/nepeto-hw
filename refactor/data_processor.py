from datetime import datetime
from typing import List, Dict, Any
from models import MarterTrackerProductHistory


class ProductDataProcessor:
    @staticmethod
    def create_history_records(
            response_data: Dict[str, Any],
            item_id: str) -> List[MarterTrackerProductHistory]:
        try:
            price_history = response_data['result'][0]['stats'][
                'low_price_history']
        except (KeyError, IndexError):
            raise ValueError(
                f"Invalid response data structure for item {item_id}")

        return [
            MarterTrackerProductHistory(
                item_id=item_id,
                date=datetime.fromtimestamp(price_point.get('timestamp', 0)),
                review_count=-1,
                rating=-1,
                offers="",
                current_seller={},
                current_stock={},
                current_price={
                    "price": price_point.get('price', -1),
                    "price_lowest": price_point.get('price', -1),
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
            for price_point in price_history
        ]
