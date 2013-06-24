from bson import ObjectId
import pymongo


class Database(object):
    def __init__(self, host, port, database):
        mongo = pymongo.MongoClient(host, port)
        self.db = mongo[database]

    def save(self, collection_name, object_to_save):
        record_id = self.db[collection_name].insert(object_to_save)
        return record_id

    def retrieve(self, collection_name, record_id):
        record = self.db[collection_name].find_one(
            {'_id': ObjectId(oid=record_id)})
        print record, '<-----------------------------------', record_id
        self._make_id_safe(record)
        return record

    def _make_id_safe(self, record):
        record['_id'] = str(record['_id'])

    def retrieve_all(self, collection_name):
        records = list(self.db[collection_name].find())
        for record in records:
            self._make_id_safe(record)
        return records
