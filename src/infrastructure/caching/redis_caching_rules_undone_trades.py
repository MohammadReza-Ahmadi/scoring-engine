from typing import List

from redis import StrictRedis

from data.rule.undone.rules_undone_arrear_trades_counts import RuleUnDoneArrearTradesCount
from data.rule.undone.rules_undone_arrear_trades_total_balance_of_last_year_ratios import RuleUnDoneArrearTradesTotalBalanceOfLastYearRatio
from data.rule.undone.rules_undone_past_due_trades_counts import RuleUnDonePastDueTradesCount
from data.rule.undone.rules_undone_past_due_trades_total_balance_of_last_year_ratios import RuleUnDonePastDueTradesTotalBalanceOfLastYearRatio
from data.rule.undone.rules_undone_undue_trades_counts import RuleUnDoneUndueTradesCount
from data.rule.undone.rules_undone_undue_trades_total_balance_of_last_year_ratios import RuleUnDoneUndueTradesTotalBalanceOfLastYearRatio
from infrastructure.constants import rules_max_val, rules_min_val, \
    SET_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, SET_RULES_UNDONE_ARREAR_TRADES_COUNTS, SET_RULES_UNDONE_PAST_DUE_TRADES_COUNTS, \
    SET_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, SET_RULES_UNDONE_UNDUE_TRADES_COUNTS, \
    SET_RULES_UNDONE_UNDUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS
from service.util import get_score_from_dict, add_rule_model_to_dict


# noinspection DuplicatedCode
class RedisCachingRulesUndoneTrades:
    recreate_caches = True
    rds: [StrictRedis] = None

    def cache_rules(self, rds: StrictRedis):
        self.rds = rds
        self.cache_rules_undone_arrear_trades_counts()
        self.cache_rules_undone_arrear_trades_total_balance_of_last_year_ratios()
        self.cache_rules_undone_past_due_trades_counts()
        self.cache_rules_undone_past_due_trades_total_balance_of_last_year_ratios()
        self.cache_rules_undone_undue_trades_counts()
        self.cache_rules_undone_undue_trades_total_balance_of_last_year_ratios()

    # ---------------------------- set cache methods ----------------------------------- #
    def cache_rules_undone_arrear_trades_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_ARREAR_TRADES_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_ARREAR_TRADES_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDoneArrearTradesCount] = RuleUnDoneArrearTradesCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_ARREAR_TRADES_COUNTS, rdict)
        print('caching rules_undone_arrear_trades_counts are done.')

    def cache_rules_undone_arrear_trades_total_balance_of_last_year_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDoneArrearTradesTotalBalanceOfLastYearRatio] = RuleUnDoneArrearTradesTotalBalanceOfLastYearRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rdict)
        print('caching rules_undone_arrear_trades_total_balance_of_last_year_ratios are done.')

    def cache_rules_undone_past_due_trades_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_PAST_DUE_TRADES_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_PAST_DUE_TRADES_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDonePastDueTradesCount] = RuleUnDonePastDueTradesCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_PAST_DUE_TRADES_COUNTS, rdict)
        print('caching rules_undone_past_due_trades_counts are done.')

    def cache_rules_undone_past_due_trades_total_balance_of_last_year_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDonePastDueTradesTotalBalanceOfLastYearRatio] = RuleUnDonePastDueTradesTotalBalanceOfLastYearRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rdict)
        print('caching rules_undone_past_due_trades_total_balance_of_last_year_ratios are done.')

    def cache_rules_undone_undue_trades_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_UNDUE_TRADES_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_UNDUE_TRADES_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDoneUndueTradesCount] = RuleUnDoneUndueTradesCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_UNDUE_TRADES_COUNTS, rdict)
        print('caching rules_undone_undue_trades_counts are done.')

    def cache_rules_undone_undue_trades_total_balance_of_last_year_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_UNDONE_UNDUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_UNDONE_UNDUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleUnDoneUndueTradesTotalBalanceOfLastYearRatio] = RuleUnDoneUndueTradesTotalBalanceOfLastYearRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_UNDONE_UNDUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, rdict)
        print('caching rules_undone_undue_trades_total_balance_of_last_year_ratios are done.')

    # ---------------------------- read cache methods ----------------------------------- #
    def get_score_of_rules_undone_arrear_trades_total_balance_of_last_year_ratios(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_undone_arrear_trades_counts(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_UNDONE_ARREAR_TRADES_COUNTS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_undone_past_due_trades_counts(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_UNDONE_PAST_DUE_TRADES_COUNTS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_undone_past_due_trades_total_balance_of_last_year_ratios(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, trades_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_undone_undue_trades_total_balance_of_last_year_ratios(self, trades_count):
        scores = self.rds.zrangebyscore(SET_RULES_UNDONE_UNDUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, trades_count, rules_max_val)
        return get_score_from_dict(scores)
