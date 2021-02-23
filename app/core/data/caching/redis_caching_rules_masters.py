from redis import StrictRedis

from app.core.constants import IDENTITIES, \
    SET_RULES_IDENTITIES_MASTER, SET_RULES_HISTORIES_MASTER, HISTORIES, SET_RULES_VOLUMES_MASTER, VOLUMES, SET_RULES_TIMELINESS_MASTER, TIMELINESS, \
    RDS_PERCENT, RDS_SCORE, CODE, IMPACT_PERCENT, SCORE
from app.core.models.rules import Rule
from app.core.services.data_service import DataService


# noinspection DuplicatedCode
class RedisCachingRulesMasters:
    recreate_caches = True
    rds: StrictRedis = None
    ds: DataService = None

    def __init__(self, rds: StrictRedis, ds: DataService = None) -> None:
        self.rds = rds
        self.ds = ds

    def cache_rules(self):
        self.cache_rule_identities_master()
        self.cache_rule_histories_master()
        self.cache_rule_volumes_master()
        self.cache_rule_timeliness_master()

    # ---------------------------- set cache methods ----------------------------------- #
    def cache_rule_identities_master(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_IDENTITIES_MASTER)
        if not bool(self.rds.get(SET_RULES_IDENTITIES_MASTER)):
            # rule: Rule = Rule.objects(Q(code=IDENTITIES)).first()
            rule: {} = self.ds.get_rule({CODE: IDENTITIES})
            # self.rds.hmset(SET_RULES_IDENTITIES_MASTER, {PERCENT: rule.impact_percent, SCORE: rule.score})
            self.rds.hmset(SET_RULES_IDENTITIES_MASTER, {RDS_PERCENT: rule[IMPACT_PERCENT], RDS_SCORE: rule[SCORE]})
        print('caching set_rules_identities_master are done.')

    def cache_rule_histories_master(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_HISTORIES_MASTER)
        if not bool(self.rds.get(SET_RULES_HISTORIES_MASTER)):
            # rule: Rule = Rule.objects(Q(code=HISTORIES)).first()
            rule: Rule = self.ds.get_rule({CODE: HISTORIES})
            self.rds.hmset(SET_RULES_HISTORIES_MASTER, {RDS_PERCENT: rule[IMPACT_PERCENT], RDS_SCORE: rule[SCORE]})
        print('caching set_rules_histories_master are done.')

    def cache_rule_volumes_master(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_VOLUMES_MASTER)
        if not bool(self.rds.get(SET_RULES_VOLUMES_MASTER)):
            # rule: Rule = Rule.objects(Q(code=VOLUMES)).first()
            rule: Rule = self.ds.get_rule({CODE: VOLUMES})
            self.rds.hmset(SET_RULES_VOLUMES_MASTER, {RDS_PERCENT: rule[IMPACT_PERCENT], RDS_SCORE: rule[SCORE]})
        print('caching set_rules_volumes_master are done.')

    def cache_rule_timeliness_master(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_TIMELINESS_MASTER)
        if not bool(self.rds.get(SET_RULES_TIMELINESS_MASTER)):
            # rule: Rule = Rule.objects(Q(code=TIMELINESS)).first()
            rule: Rule = self.ds.get_rule({CODE: TIMELINESS})
            self.rds.hmset(SET_RULES_TIMELINESS_MASTER, {RDS_PERCENT: rule[IMPACT_PERCENT], RDS_SCORE: rule[SCORE]})
        print('caching set_rules_timeliness_master are done.')

    # ---------------------------- read cache methods ----------------------------------- #
    def get_impact_percent_of_rule_identities_master(self):
        return self.rds.hget(SET_RULES_IDENTITIES_MASTER, RDS_PERCENT)

    def get_score_of_rule_identities_master(self):
        return self.rds.hget(SET_RULES_IDENTITIES_MASTER, RDS_SCORE)

    def get_impact_percent_of_rule_histories_master(self):
        return self.rds.hget(SET_RULES_HISTORIES_MASTER, RDS_PERCENT)

    def get_score_of_rule_histories_master(self):
        return self.rds.hget(SET_RULES_HISTORIES_MASTER, RDS_SCORE)

    def get_impact_percent_of_rule_volumes_master(self):
        return self.rds.hget(SET_RULES_VOLUMES_MASTER, RDS_PERCENT)

    def get_score_of_rule_volumes_master(self):
        return self.rds.hget(SET_RULES_VOLUMES_MASTER, RDS_SCORE)

    def get_impact_percent_of_rule_timeliness_master(self):
        return self.rds.hget(SET_RULES_TIMELINESS_MASTER, RDS_PERCENT)

    def get_score_of_rule_timeliness_master(self):
        return self.rds.hget(SET_RULES_TIMELINESS_MASTER, RDS_SCORE)
