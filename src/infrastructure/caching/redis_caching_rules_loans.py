from typing import List

from redis import StrictRedis

from data.rule.loan.rules_arrear_loans_total_balance_ratios import RuleArrearLoansTotalBalanceRatio
from data.rule.loan.rules_arrear_loans_total_counts import RuleArrearLoansTotalCount
from data.rule.loan.rules_loan_monthly_installments_total_balance_ratios import RuleLoanMonthlyInstallmentsTotalBalanceRatio
from data.rule.loan.rules_loans_total_counts import RuleLoansTotalCount
from data.rule.loan.rules_overdue_loans_total_balance_ratios import RuleOverdueLoansTotalBalanceRatio
from data.rule.loan.rules_past_due_loans_total_balance_ratios import RulePastDueLoansTotalBalanceRatio
from data.rule.loan.rules_past_due_loans_total_counts import RulePastDueLoansTotalCount
from data.rule.loan.rules_suspicious_loans_total_balance_ratios import RuleSuspiciousLoansTotalBalanceRatio
from data.rule.loan.rules_suspicious_loans_total_counts import RuleSuspiciousLoansTotalCount
from infrastructure.constants import rules_max_val, rules_min_val, \
    SET_RULES_ARREAR_LOANS_TOTAL_BALANCE_RATIOS, SET_RULES_ARREAR_LOANS_TOTAL_COUNTS, SET_RULES_LOAN_MONTHLY_INSTALLMENTS_TOTAL_BALANCE_RATIOS, \
    SET_RULES_LOANS_TOTAL_COUNTS, SET_RULES_OVERDUE_LOANS_TOTAL_BALANCE_RATIOS, SET_RULES_PAST_DUE_LOANS_TOTAL_BALANCE_RATIOS, \
    SET_RULES_PAST_DUE_LOANS_TOTAL_COUNTS, SET_RULES_SUSPICIOUS_LOANS_TOTAL_BALANCE_RATIOS, SET_RULES_SUSPICIOUS_LOANS_TOTAL_COUNTS
from service.util import add_rule_model_to_dict, get_score_from_dict


# noinspection DuplicatedCode
class RedisCachingRulesLoans:
    recreate_caches = True
    rds: [StrictRedis] = None

    def __init__(self, rds: StrictRedis) -> None:
        self.rds = rds
        super().__init__()

    def cache_rules(self):
        self.cache_rules_arrear_loans_total_balance_ratios()
        self.cache_rules_arrear_loans_total_counts()
        self.cache_rules_loan_monthly_installments_total_balance_ratios()
        self.cache_rules_loans_total_counts()
        self.cache_rules_overdue_loans_total_balance_ratios()
        self.cache_rules_past_due_loans_total_balance_ratios()
        self.cache_rules_past_due_loans_total_counts()
        self.cache_rules_suspicious_loans_total_balance_ratios()
        self.cache_rules_suspicious_loans_total_counts()

    # ---------------------------- set cache methods ----------------------------------- #
    def cache_rules_arrear_loans_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_ARREAR_LOANS_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_ARREAR_LOANS_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleArrearLoansTotalBalanceRatio] = RuleArrearLoansTotalBalanceRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_ARREAR_LOANS_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_arrear_loans_total_balance_ratios are done.')

    def cache_rules_arrear_loans_total_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_ARREAR_LOANS_TOTAL_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_ARREAR_LOANS_TOTAL_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleArrearLoansTotalCount] = RuleArrearLoansTotalCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_ARREAR_LOANS_TOTAL_COUNTS, rdict)
        print('caching rules_arrear_loans_total_counts are done.')

    def cache_rules_loan_monthly_installments_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_LOAN_MONTHLY_INSTALLMENTS_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_LOAN_MONTHLY_INSTALLMENTS_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleLoanMonthlyInstallmentsTotalBalanceRatio] = RuleArrearLoansTotalCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_LOAN_MONTHLY_INSTALLMENTS_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_loan_monthly_installments_total_balance_ratios are done.')

    def cache_rules_loans_total_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_LOANS_TOTAL_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_LOANS_TOTAL_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleLoansTotalCount] = RuleLoansTotalCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_LOANS_TOTAL_COUNTS, rdict)
        print('caching rules_loans_total_counts are done.')

    def cache_rules_overdue_loans_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_OVERDUE_LOANS_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_OVERDUE_LOANS_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleOverdueLoansTotalBalanceRatio] = RuleOverdueLoansTotalBalanceRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_OVERDUE_LOANS_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_overdue_loans_total_balance_ratios are done.')

    def cache_rules_past_due_loans_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PAST_DUE_LOANS_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_PAST_DUE_LOANS_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RulePastDueLoansTotalBalanceRatio] = RulePastDueLoansTotalBalanceRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_PAST_DUE_LOANS_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_past_due_loans_total_balance_ratios are done.')

    def cache_rules_past_due_loans_total_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_PAST_DUE_LOANS_TOTAL_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_PAST_DUE_LOANS_TOTAL_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RulePastDueLoansTotalCount] = RulePastDueLoansTotalCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_PAST_DUE_LOANS_TOTAL_COUNTS, rdict)
        print('caching rules_past_due_loans_total_counts are done.')

    def cache_rules_suspicious_loans_total_balance_ratios(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_SUSPICIOUS_LOANS_TOTAL_BALANCE_RATIOS)
        if not bool(self.rds.zcount(SET_RULES_SUSPICIOUS_LOANS_TOTAL_BALANCE_RATIOS, rules_min_val, rules_max_val)):
            rules: List[RuleSuspiciousLoansTotalBalanceRatio] = RuleSuspiciousLoansTotalBalanceRatio.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_SUSPICIOUS_LOANS_TOTAL_BALANCE_RATIOS, rdict)
        print('caching rules_suspicious_loans_total_balance_ratios are done.')

    def cache_rules_suspicious_loans_total_counts(self):
        if self.recreate_caches:
            self.rds.delete(SET_RULES_SUSPICIOUS_LOANS_TOTAL_COUNTS)
        if not bool(self.rds.zcount(SET_RULES_SUSPICIOUS_LOANS_TOTAL_COUNTS, rules_min_val, rules_max_val)):
            rules: List[RuleSuspiciousLoansTotalCount] = RuleSuspiciousLoansTotalCount.objects()
            rdict = {}
            for r in rules:
                add_rule_model_to_dict(rdict, r)
            self.rds.zadd(SET_RULES_SUSPICIOUS_LOANS_TOTAL_COUNTS, rdict)
        print('caching rules_suspicious_loans_total_counts are done.')

    # ---------------------------- read cache methods ----------------------------------- #
    def get_score_of_rules_arrear_loans_total_balance_ratios(self, arrear_total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_ARREAR_LOANS_TOTAL_BALANCE_RATIOS, arrear_total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_arrear_loans_total_counts(self, arrear_loans_total_count):
        scores = self.rds.zrangebyscore(SET_RULES_ARREAR_LOANS_TOTAL_COUNTS, arrear_loans_total_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_loan_monthly_installments_total_balance_ratios(self, installments_total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_LOAN_MONTHLY_INSTALLMENTS_TOTAL_BALANCE_RATIOS, installments_total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_loans_total_counts(self, loans_total_count):
        scores = self.rds.zrangebyscore(SET_RULES_LOANS_TOTAL_COUNTS, loans_total_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_overdue_loans_total_balance_ratios(self, overdue_total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_OVERDUE_LOANS_TOTAL_BALANCE_RATIOS, overdue_total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_past_due_loans_total_balance_ratios(self, past_due_total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_PAST_DUE_LOANS_TOTAL_BALANCE_RATIOS, past_due_total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_past_due_loans_total_counts(self, past_due_loans_total_count):
        scores = self.rds.zrangebyscore(SET_RULES_PAST_DUE_LOANS_TOTAL_COUNTS, past_due_loans_total_count, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_suspicious_loans_total_balance_ratios(self, suspicious_total_balance_ratio):
        scores = self.rds.zrangebyscore(SET_RULES_SUSPICIOUS_LOANS_TOTAL_BALANCE_RATIOS, suspicious_total_balance_ratio, rules_max_val)
        return get_score_from_dict(scores)

    def get_score_of_rules_suspicious_loans_total_counts(self, suspicious_loans_total_count):
        scores = self.rds.zrangebyscore(SET_RULES_SUSPICIOUS_LOANS_TOTAL_COUNTS, suspicious_loans_total_count, rules_max_val)
        return get_score_from_dict(scores)
