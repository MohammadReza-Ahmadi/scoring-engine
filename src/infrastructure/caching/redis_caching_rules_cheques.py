from typing import List

from redis import StrictRedis

from data.rule.cheque.rules_cheque_unfixed_returned_count_between_last_3_to_12_months import RuleUnfixedReturnedChequesCountBetweenLast3To12Months
from data.rule.cheque.rules_cheque_unfixed_returned_count_of_last_3_months import RuleUnfixedReturnedChequesCountOfLast3Months
from data.rule.cheque.rules_cheque_unfixed_returned_count_of_last_5_years import RuleUnfixedReturnedChequesCountOfLast5Years
from data.rule.cheque.rules_cheque_unfixed_returned_count_of_more_12_months import RuleUnfixedReturnedChequesCountOfMore12Months
from data.rule.cheque.rules_cheque_unfixed_returned_total_balance_ratios import RuleUnfixedReturnedChequesTotalBalanceRatios
from infrastructure.constants import rules_max_val, rules_min_val, \
    SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_BETWEEN_LAST_3_TO_12_MONTHS, SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_3_MONTHS, \
    SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_5_YEARS, SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_MORE_12_MONTHS, \
    SET_RULES_CHEQUE_UNFIXED_RETURNED_TOTAL_BALANCE_RATIOS
from service.util import add_rule_model_to_dict, get_score_from_dict


# noinspection DuplicatedCode
class RedisCachingRulesCheques:
    recreate_caches = True
    rds: [StrictRedis] = None

    def __init__(self, rds: StrictRedis) -> None:
        self.rds = rds
        super().__init__()

    def cache_rules(self):
        self.cache_rules_unfixed_returned_cheques_count_between_last_3_to_12_months()
        self.cache_rules_unfixed_returned_cheques_count_of_last_3_months()
        self.cache_rules_unfixed_returned_cheques_count_of_last_5_years()
        self.cache_rules_unfixed_returned_cheques_count_of_more_12_months()
        self.cache_rules_unfixed_returned_cheques_total_balance_ratios()

    # ---------------------------- set cache methods ----------------------------------- #
    def cache_rules_unfixed_returned_cheques_count_between_last_3_to_12_months(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_BETWEEN_LAST_3_TO_12_MONTHS)
        if not bool(self.rds.zcount(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_BETWEEN_LAST_3_TO_12_MONTHS, rules_min_val, rules_max_val)):
            rules: List[RuleUnfixedReturnedChequesCountBetweenLast3To12Months] = RuleUnfixedReturnedChequesCountBetweenLast3To12Months.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_BETWEEN_LAST_3_TO_12_MONTHS, rdict)
        print('caching rules_unfixed_returned_cheques_count_between_last_3_to_12_months are done.')

    def cache_rules_unfixed_returned_cheques_count_of_last_3_months(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_3_MONTHS)
        if not bool(self.rds.zcount(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_3_MONTHS, rules_min_val, rules_max_val)):
            rules: List[RuleUnfixedReturnedChequesCountOfLast3Months] = RuleUnfixedReturnedChequesCountOfLast3Months.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_3_MONTHS, rdict)
        print('caching rules_unfixed_returned_cheques_count_of_last_3_months are done.')

    def cache_rules_unfixed_returned_cheques_count_of_last_5_years(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_5_YEARS)
        if not bool(self.rds.zcount(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_5_YEARS, rules_min_val, rules_max_val)):
            rules: List[RuleUnfixedReturnedChequesCountOfLast5Years] = RuleUnfixedReturnedChequesCountOfLast5Years.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_5_YEARS, rdict)
        print('caching rules_unfixed_returned_cheques_count_of_last_5_years are done.')

    def cache_rules_unfixed_returned_cheques_count_of_more_12_months(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_MORE_12_MONTHS)
        if not bool(self.rds.zcount(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_MORE_12_MONTHS, rules_min_val, rules_max_val)):
            rules: List[RuleUnfixedReturnedChequesCountOfMore12Months] = RuleUnfixedReturnedChequesCountOfMore12Months.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_MORE_12_MONTHS, rdict)
        print('caching rules_unfixed_returned_cheques_count_of_more_12_months are done.')

    def cache_rules_unfixed_returned_cheques_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_CHEQUE_UNFIXED_RETURNED_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_CHEQUE_UNFIXED_RETURNED_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleUnfixedReturnedChequesTotalBalanceRatios] = RuleUnfixedReturnedChequesTotalBalanceRatios.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_CHEQUE_UNFIXED_RETURNED_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_unfixed_returned_cheques_total_balance_ratios are done.')

    # ---------------------------- read cache methods ----------------------------------- #
    def get_score_of_rules_unfixed_returned_cheques_count_between_last_3_to_12_months(self, cheque_count):
        scores = self.rds.zrangebyscore(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_BETWEEN_LAST_3_TO_12_MONTHS, cheque_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_unfixed_returned_cheques_count_of_last_3_months(self, cheque_count):
        scores = self.rds.zrangebyscore(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_3_MONTHS, cheque_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_unfixed_returned_cheques_count_of_last_5_years(self, cheque_count):
        scores = self.rds.zrangebyscore(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_LAST_5_YEARS, cheque_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_unfixed_returned_cheques_count_of_more_12_months(self, cheque_count):
        scores = self.rds.zrangebyscore(SET_RULES_CHEQUE_UNFIXED_RETURNED_COUNT_OF_MORE_12_MONTHS, cheque_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_unfixed_returned_cheques_total_balance_ratios(self, total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_CHEQUE_UNFIXED_RETURNED_TOTAL_BALANCE_RATIOS, total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)
