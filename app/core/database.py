from pymongo import MongoClient

from app.core.settings import mongodb_user, mongodb_pass, mongodb_host, mongodb_port, mongodb_name


def get_db():
    client = MongoClient('mongodb://' + mongodb_user + ':' + mongodb_pass + '@' + mongodb_host + ':' + str(mongodb_port))
    return client.get_database(mongodb_name)
