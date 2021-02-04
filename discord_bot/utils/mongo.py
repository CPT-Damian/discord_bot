import logging
import collections


class Document:
    def __init__(self, connection, document_name):
        """
        Our init functions sets up the connection to the specified document
        Params:
        - connection (Mongo Connection): Our database connection
        - documentName (str): The document this instance should be
        """
        self.db = connection[document_name]
        self.logger = logging.getLogger(__name__)

    async def update(self, dict):
        """
        For simpler calls, points to self.update_by_id
        :param dict:
        :return:
        """
        await self.update_by_id(dict)

    async def get_by_id(self, id):
        """
        This is essentially find_by_id so it points to that
        :param id:
        :return:
        """
        return await self.find_by_id(id)

    async def find(self, id):
        """
        for simpler calls, points to self.find_by_id
        :param id:
        :return:
        """
        return await self.find_by_id(id)

    async def delete(self, id):
        """
        For simpler calls, points to self.delete_by_id
        """
        await self.delete_by_id(id)

    async def find_by_id(self, id):
        """
        Returns the data found under 'id'

        Params:
        - id (): The id to search for

        Returns:
        - None if nothing is found
        - If somethings found, return that
        """
        return await self.db.find_one({"_id": id})

    async def delete_by_id(self, id):
        """
        Deletes all items found with _id: 'id'

        Params:
        -id (): The id to search for and delete
        :param id:
        :return:
        """
        if not await self.find_by_id(id):
            pass

        await self.db.delete_many({"_id": id})

    async def insert(self, dict):
        """
        insert something into the db

        Params:
        - dict (Dictionary): The dictionary to insert
        """
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")
        if not dict["_id"]:
            raise KeyError("_id not found in supplied dict.")
        await self.db.insert_one(dict)

    async def upsert(self, dict):
        if await self.__get_raw(dict["_id"]) != None:
            await self.update_by_id(dict)
        else:
            await self.db.insert_one(dict)

    async def update_by_id(self, dict):
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        if not dict["_id"]:
            raise KeyError("_id not found in supplied dict.")

        if not await self.find_by_id(dict["_id"]):
            pass

        id = dict["_id"]
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$set": dict})

    async def unset(self, dict):
        if not isinstance(dict, collections.abc.Mapping):
            raise TypeError("Expected Dictionary.")

        if not dict["_id"]:
            raise KeyError("_id not found in supplied dict.")

        if not await self.find_by_id(dict["_id"]):
            return

        id = dict["_id"]
        dict.pop("_id")
        await self.db.update_one({"_id": id}, {"$unset": dict})

    async def increment(self, id, amount, field):
        if not await self.find_by_id(id):
            pass

        self.db.update_one({"_id": id}, {"$inc": {field: amount}})

    async def get_all(self):
        data = []
        async for document in self.db.find({}):
            data.append(document)
        return data

    async def __get_raw(self, id):
        return await self.db.find_one({"_id": id})