import redis
from redis import StrictRedis

import program
from infrastructure.caching.redis_caching_rules_cheques import RedisCachingRulesCheques
from infrastructure.caching.redis_caching_rules_done_trades import RedisCachingRulesDoneTrades
from infrastructure.caching.redis_caching_rules_loans import RedisCachingRulesLoans
from infrastructure.caching.redis_caching_rules_masters import RedisCachingRulesMasters
from infrastructure.caching.redis_caching_rules_profiles import RedisCachingRulesProfiles
from infrastructure.caching.redis_caching_rules_undone_trades import RedisCachingRulesUndoneTrades
from infrastructure.constants import redis_password


# noinspection DuplicatedCode


class RedisCaching:
    recreate_caches = True
    rds: [StrictRedis] = None
    rds_rules_profile_service = None
    rds_rules_done_trades_service = None
    rds_rules_undone_trades_service = None
    rds_rules_cheques_service = None
    rds_rules_loans_service = None

    def __init__(self):
        try:
            pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password=redis_password, decode_responses=True)
            self.rds = redis.StrictRedis(connection_pool=pool)
            print("credit-scoring redis connection is established.")
        except Exception as e:
            print(e)

    def get_redis_caching_rules_profile_service(self, reset_cache=False):
        if self.rds_rules_profile_service is None:
            self.rds_rules_profile_service = RedisCachingRulesProfiles(self.rds)
        if reset_cache:
            self.rds_rules_profile_service.cache_rules()
        return self.rds_rules_profile_service

    def get_redis_caching_rules_done_trades_service(self, reset_cache=False):
        if self.rds_rules_done_trades_service is None:
            self.rds_rules_done_trades_service = RedisCachingRulesDoneTrades(self.rds)
        if reset_cache:
            self.rds_rules_done_trades_service.cache_rules()
        return self.rds_rules_done_trades_service

    def get_redis_caching_rules_undone_trades_service(self, reset_cache=False):
        if self.rds_rules_undone_trades_service is None:
            self.rds_rules_undone_trades_service = RedisCachingRulesUndoneTrades(self.rds)
        if reset_cache:
            self.rds_rules_undone_trades_service.cache_rules()
        return self.rds_rules_undone_trades_service

    def get_redis_caching_rules_cheques_service(self, reset_cache=False):
        if self.rds_rules_cheques_service is None:
            self.rds_rules_cheques_service = RedisCachingRulesCheques(self.rds)
        if reset_cache:
            self.rds_rules_cheques_service.cache_rules()
        return self.rds_rules_cheques_service

    def get_redis_caching_rules_loans_service(self, reset_cache=False):
        if self.rds_rules_loans_service is None:
            self.rds_rules_loans_service = RedisCachingRulesLoans(self.rds)
        if reset_cache:
            self.rds_rules_loans_service.cache_rules()
        return self.rds_rules_loans_service

    def cache_rules(self):
        RedisCachingRulesMasters(self.rds).cache_rules()
        RedisCachingRulesDoneTrades(self.rds).cache_rules()
        RedisCachingRulesUndoneTrades(self.rds).cache_rules()
        RedisCachingRulesProfiles(self.rds).cache_rules()
        RedisCachingRulesLoans(self.rds).cache_rules()
        RedisCachingRulesCheques(self.rds).cache_rules()


if __name__ == '__main__':
    program.launch_app()
    RedisCaching().cache_rules()
