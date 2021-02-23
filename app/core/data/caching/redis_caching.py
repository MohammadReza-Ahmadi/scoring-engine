import redis
from redis import StrictRedis

from app.core.data.caching.redis_caching_rules_cheques import RedisCachingRulesCheques
from app.core.data.caching.redis_caching_rules_done_trades import RedisCachingRulesDoneTrades
from app.core.data.caching.redis_caching_rules_loans import RedisCachingRulesLoans
from app.core.data.caching.redis_caching_rules_masters import RedisCachingRulesMasters
from app.core.data.caching.redis_caching_rules_profiles import RedisCachingRulesProfiles
from app.core.data.caching.redis_caching_rules_undone_trades import RedisCachingRulesUndoneTrades
from app.core.services.data_service import DataService
from app.core.settings import redis_host, redis_pass, redis_port, mongodb_name


# noinspection DuplicatedCode
class RedisCaching:
    recreate_caches = True
    rds: StrictRedis = None
    rds_rules_profile_service = None
    rds_rules_done_trades_service = None
    rds_rules_undone_trades_service = None
    rds_rules_cheques_service = None
    rds_rules_loans_service = None

    def __init__(self, ds: DataService):
        try:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)
            self.rds = redis.StrictRedis(connection_pool=pool)
            self.ds = ds
            print("{} redis connection is established.".format(mongodb_name))
        except Exception as e:
            print(e)

    def get_redis_caching_rules_profile_service(self, reset_cache=False):
        if self.rds_rules_profile_service is None:
            self.rds_rules_profile_service = RedisCachingRulesProfiles(self.rds, self.ds)
        if reset_cache:
            self.rds_rules_profile_service.cache_rules()
        return self.rds_rules_profile_service

    def get_redis_caching_rules_done_trades_service(self, reset_cache=False):
        if self.rds_rules_done_trades_service is None:
            self.rds_rules_done_trades_service = RedisCachingRulesDoneTrades(self.rds, self.ds)
        if reset_cache:
            self.rds_rules_done_trades_service.cache_rules()
        return self.rds_rules_done_trades_service

    def get_redis_caching_rules_undone_trades_service(self, reset_cache=False):
        if self.rds_rules_undone_trades_service is None:
            self.rds_rules_undone_trades_service = RedisCachingRulesUndoneTrades(self.rds, self.ds)
        if reset_cache:
            self.rds_rules_undone_trades_service.cache_rules()
        return self.rds_rules_undone_trades_service

    def get_redis_caching_rules_loans_service(self, reset_cache=False):
        if self.rds_rules_loans_service is None:
            self.rds_rules_loans_service = RedisCachingRulesLoans(self.rds, self.ds)
        if reset_cache:
            self.rds_rules_loans_service.cache_rules()
        return self.rds_rules_loans_service

    def get_redis_caching_rules_cheques_service(self, reset_cache=False):
        if self.rds_rules_cheques_service is None:
            self.rds_rules_cheques_service = RedisCachingRulesCheques(self.rds, self.ds)
        if reset_cache:
            self.rds_rules_cheques_service.cache_rules()
        return self.rds_rules_cheques_service

    def cache_rules(self):
        RedisCachingRulesMasters(self.rds, self.ds).cache_rules()
        RedisCachingRulesProfiles(self.rds, self.ds).cache_rules()
        RedisCachingRulesDoneTrades(self.rds, self.ds).cache_rules()
        RedisCachingRulesUndoneTrades(self.rds, self.ds).cache_rules()
        RedisCachingRulesLoans(self.rds, self.ds).cache_rules()
        RedisCachingRulesCheques(self.rds, self.ds).cache_rules()


if __name__ == '__main__':
    RedisCaching(DataService()).cache_rules()
