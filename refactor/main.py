import asyncio
from typing import List
from database import DatabaseManager
from api_client import DataSparkClient
from data_processor import ProductDataProcessor
from models import MarterTrackerProduct
from sqlalchemy.exc import IntegrityError


class ProductHistoryManager:
    def __init__(
            self,
            db_manager: DatabaseManager,
            api_client: DataSparkClient):
        self.db_manager = db_manager
        self.api_client = api_client
        self.processor = ProductDataProcessor()

    async def process_items(self, item_ids: List[str]):
        with self.db_manager.get_session() as session:
            for item_id in item_ids:
                try:
                    product = MarterTrackerProduct(item_id=item_id.strip())
                    session.add(product)
                    session.commit()
                except IntegrityError:
                    session.rollback()

        product_data = await self.api_client.get_bulk_product_data(item_ids)

        with self.db_manager.get_session() as session:
            for item_id, data in zip(item_ids, product_data):
                if isinstance(data, Exception):
                    print(f"Error processing item {item_id}: {data}")
                    continue

                try:
                    history_records = self.processor.create_history_records(
                        data, item_id)
                    for record in history_records:
                        try:
                            session.add(record)
                            session.commit()
                        except IntegrityError:
                            session.rollback()
                except Exception as e:
                    print(f"Error processing history for item {item_id}: {e}")


async def main():
    db_manager = DatabaseManager('postgresql://root:1234@localhost:5432/test')
    db_manager.init_db()

    api_client = DataSparkClient(api_key='717d12a2ffbfa6752e91ae36f9687284')
    manager = ProductHistoryManager(db_manager, api_client)

    item_ids = ['46480251', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    await manager.process_items(item_ids)

if __name__ == "__main__":
    asyncio.run(main())
