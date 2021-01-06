from typing import List

from redis import StrictRedis

from data.rule.profile.rules_profile_address_verifications import RuleProfileAddressVerification
from data.rule.profile.rules_profile_has_kycs import RuleProfileHasKyc
from data.rule.profile.rules_profile_membership_days_counts import RuleProfileMembershipDaysCount
from data.rule.profile.rules_profile_military_service_status import RuleProfileMilitaryServiceStatus
from data.rule.profile.rules_profile_recommended_to_others_counts import RuleProfileRecommendedToOthersCount
from data.rule.profile.rules_profile_sim_card_ownerships import RuleProfileSimCardOwnership
from data.rule.profile.rules_profile_star_counts_avgs import RuleProfileStarCountAvg
from infrastructure.constants import rules_max_val, rules_min_val, \
    SET_RULES_PROFILE_HAS_KYCS, SET_RULES_PROFILE_ADDRESS_VERIFICATIONS, SET_RULES_PROFILE_MEMBERSHIP_DAYS_COUNTS, \
    SET_RULES_PROFILE_MILITARY_SERVICE_STATUS, SET_RULES_PROFILE_RECOMMENDED_TO_OTHERS_COUNTS, SET_RULES_PROFILE_SIM_CARD_OWNERSHIPS, \
    SET_RULES_PROFILE_STAR_COUNTS_AVGS
from service.util import get_score_from_dict, add_rule_model_to_dict_by_rds_score, add_rule_model_to_dict


# noinspection DuplicatedCode
class RedisCachingRulesProfiles:
    recreate_caches = True
    rds: [StrictRedis] = None

    def cache_rules(self, rds: StrictRedis):
        self.rds = rds
        self.cache_rules_profile_address_verifications()
        self.cache_rules_profile_has_kycs()
        self.cache_rules_profile_membership_days_counts()
        self.cache_rules_profile_military_service_status()
        self.cache_rules_profile_recommended_to_others_counts()
        self.cache_rules_profile_sim_card_ownerships()
        self.cache_rules_profile_star_counts_avgs()

    # ---------------------------- set cache methods ----------------------------------- #
    def cache_rules_profile_has_kycs(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_HAS_KYCS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_HAS_KYCS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileHasKyc] = RuleProfileHasKyc.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict_by_rds_score(rdict, r, int(r.status_code))
            self.rds.zadd(SET_RULES_PROFILE_HAS_KYCS, rdict)
        print('caching rules_profile_has_kycs are done.')

    def cache_rules_profile_address_verifications(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_ADDRESS_VERIFICATIONS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_ADDRESS_VERIFICATIONS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileAddressVerification] = RuleProfileAddressVerification.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict_by_rds_score(rdict, r, int(r.status_code))
            self.rds.zadd(SET_RULES_PROFILE_ADDRESS_VERIFICATIONS, rdict)
        print('caching rules_profile_address_verifications are done.')

    def cache_rules_profile_membership_days_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_MEMBERSHIP_DAYS_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_MEMBERSHIP_DAYS_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileMembershipDaysCount] = RuleProfileMembershipDaysCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_PROFILE_MEMBERSHIP_DAYS_COUNTS, rdict)
        print('caching rules_profile_membership_days_counts are done.')

    def cache_rules_profile_military_service_status(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_MILITARY_SERVICE_STATUS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_MILITARY_SERVICE_STATUS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileMilitaryServiceStatus] = RuleProfileMilitaryServiceStatus.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict_by_rds_score(rdict, r, int(r.status_code))
            self.rds.zadd(SET_RULES_PROFILE_MILITARY_SERVICE_STATUS, rdict)
        print('caching rules_profile_military_service_status are done.')

    def cache_rules_profile_recommended_to_others_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_RECOMMENDED_TO_OTHERS_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_RECOMMENDED_TO_OTHERS_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileRecommendedToOthersCount] = RuleProfileRecommendedToOthersCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_PROFILE_RECOMMENDED_TO_OTHERS_COUNTS, rdict)
        print('caching rules_profile_recommended_to_others_counts are done.')

    def cache_rules_profile_sim_card_ownerships(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_SIM_CARD_OWNERSHIPS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_SIM_CARD_OWNERSHIPS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileSimCardOwnership] = RuleProfileSimCardOwnership.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict_by_rds_score(rdict, r, int(r.status_code))
            self.rds.zadd(SET_RULES_PROFILE_SIM_CARD_OWNERSHIPS, rdict)
        print('caching rules_profile_sim_card_ownerships are done.')

    def cache_rules_profile_star_counts_avgs(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PROFILE_STAR_COUNTS_AVGS)
        if not bool(self.rds.zcount(SET_RULES_PROFILE_STAR_COUNTS_AVGS, rules_min_val, rules_max_val)):
            rules: List[RuleProfileStarCountAvg] = RuleProfileStarCountAvg.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_PROFILE_STAR_COUNTS_AVGS, rdict)
        print('caching rules_profile_star_counts_avgs are done.')

    # ---------------------------- read cache methods ----------------------------------- #
    def get_score_of_rules_profile_has_kycs(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_HAS_KYCS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_address_verifications(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_ADDRESS_VERIFICATIONS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_membership_days_counts(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_MEMBERSHIP_DAYS_COUNTS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_military_service_status(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_MILITARY_SERVICE_STATUS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_recommended_to_others_counts(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_RECOMMENDED_TO_OTHERS_COUNTS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_sim_card_ownerships(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_SIM_CARD_OWNERSHIPS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_profile_star_counts_avgs(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_PROFILE_STAR_COUNTS_AVGS, trades_count, rules_max_val)
        return get_score_from_dict(scores)
