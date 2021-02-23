import mongoengine

# from src.infrastructure.redis_caching import cache_rules
# from infrastructure.redis_caching import RedisCaching
# from infrastructure.caching.redis_caching import cache_rules
from app.core.settings import mongodb_alias, mongodb_name, mongodb_host, mongodb_port, mongodb_user, mongodb_pass, mongodb_auth_source

mongoengine.register_connection(
    host=mongodb_host,
    port=mongodb_port,
    username=mongodb_user,
    password=mongodb_pass,
    authentication_source=mongodb_auth_source,
    db=mongodb_name,
    alias=mongodb_alias
)


def create_db_connection():
    pass


def launch_app():
    create_db_connection()
    print("credit-scoring mongodb connection is established.")
    # RedisCaching().cache_rules()


if __name__ == '__main__':
    launch_app()
