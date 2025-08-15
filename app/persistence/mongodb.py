import os
import asyncio
import uuid
from typing import Any
from bson import ObjectId
# from src.utils.console import color, color_print
from pymongo import AsyncMongoClient
from pymongo.errors import (
    AutoReconnect,
    BulkWriteError,
    CursorNotFound,
    DuplicateKeyError,
    ServerSelectionTimeoutError,
)

from app.persistence.abstract import AbstractPersistenceClient
from app.core.config import MONGO_URI, MAX_CONCURRENT_TASKS
import traceback
#from src.utils.logger import setup_json_logger

#logger = setup_json_logger(name='scraper_causas')


def color_print(text: str, **kwargs):
    print(text)



class MongoDBClient(AbstractPersistenceClient):
    
    client = None

    async def mongo_safe_query(self, **kwargs):
        if not self.client:
            self.client = AsyncMongoClient(MONGO_URI)
        if 'server' not in kwargs:
            kwargs.update({'server': self.client})
        return await self._mongo_safe_query(**kwargs)


    async def _mongo_safe_query(
        self,
        server: str,
        database: str,
        collection: str,
        function: str,
        filter: dict = {},
        projection: Any = None,
        field: str = "",
        update: dict = None,
        document: dict = None,
        upsert: bool = False,
        skip: int = 0,
        limit: int = 0,
        sort_by: str = "",
        sort_direction: int = 0,
        timeout: int = 60000,
        batch_size: int = 1000000,
        pipeline: list = [],
        distinct_key: str = "",
    ):

        query_result = None

        if server and database and collection and function:
            
            cursor = server[database][collection]
            if function in [
                "find",
                "find_one",
                "update_one",
                "update_many",
                "insert_one",
                "replace_one",
                "find_one_and_replace",
                "delete_one",
                "delete_many",
                "count_documents",
                "estimated_document_count",
                "aggregate",
                "distinct",
                "find_with_pagination",
            ]:

                try:

                    # find()
                    if function == "find":

                        try:
                            if sort_by:
                                if timeout == -1:
                                    
                                    query_results = (
                                        cursor
                                        .find(projection=projection, filter=filter)
                                        .batch_size(batch_size)
                                        .skip(skip)
                                        .limit(limit)
                                        .sort(sort_by, sort_direction)
                                    )
                                    query_results = await query_results.to_list()
                                else:
                                    query_results = (
                                        cursor
                                        .find(projection=projection, filter=filter)
                                        .batch_size(batch_size)
                                        .skip(skip)
                                        .limit(limit)
                                        .max_time_ms(timeout)
                                        .sort(sort_by, sort_direction)
                                    )
                                    query_results = await query_results.to_list()
                            else:
                                if timeout == -1:
                                    query_results = (
                                        cursor
                                        .find(projection=projection, filter=filter)
                                        .batch_size(batch_size)
                                        .skip(skip)
                                        .limit(limit)
                                    )
                                    query_results = await query_results.to_list()

                                else:
                                    query_results = (
                                        cursor
                                        .find(projection=projection, filter=filter)
                                        .batch_size(batch_size)
                                        .skip(skip)
                                        .limit(limit)
                                        .max_time_ms(timeout)
                                    )
                                    query_results = await query_results.to_list()
                            converted_list = []
                            for element in query_results:
                                if field and field in element:
                                    converted_list.append(element[field])
                                else:
                                    converted_list.append(element)
                        except Exception as e:
                            # traceback.print_exception(e)
                            color_print(str(e), color="red")
                        finally:
                            try:
                                if query_results:
                                    await query_results.close()
                            except AttributeError:
                                pass  # 'some' object has no attribute 'close'
                            except Exception as e:
                                color_print(str(e), color="red")

                        # Finish find()
                        query_result = converted_list
                        if not query_result:
                            query_result = []

                    # find_one()
                    elif function == "find_one":  # single dict (document) will be returned, cursor automatically closed.
                        query_result = await cursor.find_one(filter=filter)
                        if not query_result:
                            query_result = {}

                    # count_documents()
                    elif function == "count_documents":  # int returned, cursor automatically closed.
                        query_result = await cursor.count_documents(filter=filter)
                        if not query_result:
                            query_result = 0

                    # estimated_document_count()
                    elif function == "estimated_document_count":  # int returned, cursor automatically closed.
                        query_result = await cursor.estimated_document_count()
                        if not query_result:
                            query_result = 0

                    elif function == "aggregate":
                        query_result = 0
                        if not pipeline:
                            color_print("You must to provide an aggregation pipeline.", color="y")
                        else:
                            query_result = await cursor.aggregate(pipeline)
                            query_result = await query_result.to_list()

                    elif function == "distinct":
                        query_result = 0
                        if not distinct_key:
                            color_print("You must to provide an aggregation pipeline.", color="y")
                        else:
                            query_result = await cursor.distinct(distinct_key, filter=filter)
                            if query_result:
                                query_result = list(query_result)

                    elif function == "find_with_pagination":
                        total_documents = await cursor.estimated_document_count()
                        total_pages = int((total_documents // limit) + (1 if total_documents % limit > 0 else 0))

                        query_result = []

                        for page_number in range(total_pages + 1):
                            skip = limit * page_number
                            result = cursor.find(filter=filter, projection=projection
                                     ).sort("_id", 1).skip(skip).limit(limit).batch_size(batch_size)
                        
                            result = await result.to_list()
                            if isinstance(result, list):
                                query_result.extend(result)

                    # no documents return from these functions(), only message. cursor automatically closed.
                    elif function in [
                        "update_one",
                        "update_many",
                        "insert_one",
                        "replace_one",
                        "find_one_and_replace",
                        "delete_one",
                        "delete_many",
                    ]:
                        if function == "update_one":
                            query_result = await cursor.update_one(
                                filter=filter, update=update, upsert=upsert
                            )
                        elif function == "update_many":
                            query_result = await cursor.update_many(
                                filter=filter, update=update, upsert=upsert
                            )
                        elif function == "insert_one":
                            query_result = await cursor.insert_one(document=document)
                        elif function == "replace_one":
                            query_result = await cursor.replace_one(
                                filter=filter, replacement=document, upsert=upsert
                            )
                        elif function == "find_one_and_replace":
                            query_result = await cursor.find_one_and_replace(
                                filter=filter, projection=projection, replacement=document, upsert=upsert
                            )
                        elif function == "delete_one":
                            query_result = await cursor.delete_one(filter=filter)
                        elif function == "delete_many":
                            query_result = await cursor.delete_many(filter=filter)

                except Exception as e:
                    traceback.print_exception(e)
                    print("_ERROR: " + str(e))

        return query_result
    
    
    async def mongo_save_execution_time(self, main_task_id: str, end_time: float, start_time: float, verbose: bool = False):
        
        time_taken_in_seconds = end_time - start_time
        time_taken_in_minutes = time_taken_in_seconds / 60
        time_taken_in_hours = time_taken_in_minutes / 60
        
        if not main_task_id or not end_time or not start_time:
            raise ValueError("main_task_id, end_time and start_time are required")
        
        if verbose:
            color_print(f"\u2022 Time taken: {time_taken_in_seconds} seconds", color="GREEN")
            color_print(f"\u2022 Time taken: {time_taken_in_minutes} minutes", color="GREEN")
            color_print(f"\u2022 Time taken: {time_taken_in_hours} hours", color="GREEN")
        
        is_saved = await self.mongo_safe_query(
            database='poder_judicial',
            collection='causas_runs',
            function='insert_one',
            document={
                '_id': str(uuid.uuid4()),
                'main_task_id': main_task_id,
                'concurrency': MAX_CONCURRENT_TASKS,
                'time_taken_in_seconds': time_taken_in_seconds,
                'time_taken_in_minutes': time_taken_in_minutes,
                'time_taken_in_hours': time_taken_in_hours,
            }
        )

        return is_saved
    
    async def save_causa_detail(self, causa_metadata: dict):
        
        is_saved = await self.mongo_safe_query(
            database='poder_judicial',
            collection='causas',
            function='insert_one',
            document={
                **causa_metadata['metadata'],
                'detail': causa_metadata['detail']
            }
        )
        return is_saved

    async def save_execution_time(self, main_task_id: str, end_time: float, start_time: float, verbose: bool = False):
        return await self.mongo_save_execution_time(main_task_id=main_task_id, end_time=end_time, start_time=start_time, verbose=verbose)

    async def get_causa_by_id(self, causa_id):
        return await self.mongo_safe_query(
            database='poder_judicial',
            collection='causas',
            function='find_one',
            filter={
                '_id': ObjectId(causa_id)
            }
        )
    
    async def update_causa_detail(self, causa):
        return await super().update_causa_detail(causa)

if __name__ == '__main__':
    
    # TEST
    async def main():
    
        import json
        mongo_client = MongoDBClient()
        
       
        result = await mongo_client.mongo_safe_query(
            database='poder_judicial',
            collection='causas',
            function='delete_one',
            filter={
                '_id': ObjectId('689db57df128c34cfd80f06f')
            }
        )

        #result['_id'] = str(result['_id'])
        print(result.deleted_count)
    
    asyncio.run(main())