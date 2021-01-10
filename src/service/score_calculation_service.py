from datetime import date

from numpy import long

from data.cheques import Cheque
from data.done_trades import DoneTrade
from data.loans import Loan
from data.profile import Profile
from data.undone_trades import UndoneTrade
from infrastructure.caching.redis_caching import RedisCaching
from infrastructure.caching.redis_caching_rules_cheques import RedisCachingRulesCheques
from infrastructure.caching.redis_caching_rules_done_trades import RedisCachingRulesDoneTrades
from infrastructure.caching.redis_caching_rules_loans import RedisCachingRulesLoans
from infrastructure.caching.redis_caching_rules_profiles import RedisCachingRulesProfiles
from infrastructure.caching.redis_caching_rules_undone_trades import RedisCachingRulesUndoneTrades
from infrastructure.constants import SCORE_CODE_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS, \
    SCORE_CODE_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS


class ScoreCalculationService:

    def __init__(self, rds: RedisCaching) -> None:
        super().__init__()
        self.rds = rds

    def calculate_user_final_score(self, user_id: long):
        final_score = self.calculate_user_profile_score(user_id)
        final_score += self.calculate_user_done_trades_score(user_id)
        final_score += self.calculate_user_undone_trades_score(user_id)
        final_score += self.calculate_user_loans_score(user_id)
        final_score += self.calculate_user_cheques_score(user_id)
        print('<><><><><><><> final score = {} <><><><><><><>'.format(final_score))
        return final_score

    def calculate_user_profile_score(self, user_id: long, reset_cache=False):
        profile = Profile.objects(user_id=user_id).first()
        rds: RedisCachingRulesProfiles = self.rds.get_redis_caching_rules_profile_service(reset_cache)
        profile_score = 0
        score = rds.get_score_of_rules_profile_address_verifications(profile.address_verification)
        profile_score += score
        print('score= {}, profile:[address_verification]= {}'.format(score, profile.address_verification))
        score = rds.get_score_of_rules_profile_has_kycs(profile.has_kyc)
        profile_score += score
        print('score= {}, profile:[has_kyc]= {}'.format(score, profile.has_kyc))
        # calculate membership days count
        member_ship_days_count = (date.today() - profile.membership_date).days
        score = rds.get_score_of_rules_profile_membership_days_counts(member_ship_days_count)
        profile_score += score
        print('score= {}, profile:[membership_date]= {}, profile_member_ship_days_count={}'.format(score, profile.membership_date,
                                                                                                   member_ship_days_count))
        score = rds.get_score_of_rules_profile_military_service_status(profile.military_service_status)
        profile_score += score
        print('score= {}, profile:[military_service_status]= {}'.format(score, profile.military_service_status))
        score = rds.get_score_of_rules_profile_recommended_to_others_counts(profile.recommended_to_others_count)
        profile_score += score
        print('score= {}, profile:[recommended_to_others_count]= {}'.format(score, profile.recommended_to_others_count))
        score = rds.get_score_of_rules_profile_sim_card_ownerships(profile.sim_card_ownership)
        profile_score += score
        print('score= {}, profile:[sim_card_ownership]= {}'.format(score, profile.sim_card_ownership))
        score = rds.get_score_of_rules_profile_star_counts_avgs(profile.star_count_average)
        profile_score += score
        print('score= {}, profile:[star_count_average]= {}'.format(score, profile.star_count_average))
        print('............. profile score = {} ................\n'.format(profile_score))
        return profile_score

    def calculate_user_done_trades_score(self, user_id: long, reset_cache=False):
        done_trade: DoneTrade = DoneTrade.objects(user_id=user_id).first()
        rds: RedisCachingRulesDoneTrades = self.rds.get_redis_caching_rules_done_trades_service(reset_cache)
        done_trades_score = 0

        score = rds.get_score_of_rules_done_timely_trades_of_last_3_months(done_trade.timely_trades_count_of_last_3_months)
        done_trades_score += score
        print('score= {}, doneTrades:[timely_trades_count_of_last_3_months]= {}'.format(score, done_trade.timely_trades_count_of_last_3_months))

        score = rds.get_score_of_rules_done_timely_trades_between_last_3_to_12_months(done_trade.timely_trades_count_between_last_3_to_12_months)
        done_trades_score += score
        print('score= {}, doneTrades:[timely_trades_count_between_last_3_to_12_months]= {}'
              .format(score, done_trade.timely_trades_count_between_last_3_to_12_months))

        score = rds.get_score_of_rules_done_past_due_trades_of_last_3_months(done_trade.past_due_trades_count_of_last_3_months)
        done_trades_score += score
        print('score= {}, doneTrades:[past_due_trades_count_of_last_3_months]= {}'.format(score, done_trade.past_due_trades_count_of_last_3_months))

        score = rds.get_score_of_rules_done_past_due_trades_between_last_3_to_12_months(done_trade.past_due_trades_count_between_last_3_to_12_months)
        done_trades_score += score
        print('score= {}, doneTrades:[past_due_trades_count_between_last_3_to_12_months]= {}'.
              format(score, done_trade.past_due_trades_count_between_last_3_to_12_months))

        score = rds.get_score_of_rules_done_arrear_trades_of_last_3_months(done_trade.arrear_trades_count_of_last_3_months)
        done_trades_score += score
        print('score= {}, doneTrades:[arrear_trades_count_of_last_3_months]= {}'.format(score, done_trade.arrear_trades_count_of_last_3_months))

        score = rds.get_score_of_rules_done_arrear_trades_between_last_3_to_12_months(done_trade.arrear_trades_count_between_last_3_to_12_months)
        done_trades_score += score
        print('score= {}, doneTrades:[arrear_trades_count_between_last_3_to_12_months]= {}'
              .format(score, done_trade.arrear_trades_count_between_last_3_to_12_months))

        # calculate average of total balance
        # todo: should calculate all users' trades total balance
        avg_total_balance = done_trade.trades_total_balance / 100000000
        avg_total_balance = float(avg_total_balance)
        score = rds.get_score_of_rules_done_trades_average_total_balance_ratios(avg_total_balance)
        done_trades_score += score
        print('score= {}, doneTrades:[avg_total_balance]= {}'.format(score, avg_total_balance))

        # calculate average of all users delay days
        # todo: should calculate all users' average of done trades delay days (general_avg_delay_days)
        general_avg_delay_days = 0
        avg_delay_days = 0 if general_avg_delay_days == 0 else done_trade.total_delay_days / general_avg_delay_days
        score = rds.get_score_of_rules_done_trades_average_delay_days(avg_delay_days)
        done_trades_score += score
        print('score= {}, doneTrades:[avg_delay_days]= {}'.format(score, done_trade.total_delay_days))

        print('............. doneTrades score = {} ................\n'.format(done_trades_score))
        return done_trades_score

    def calculate_user_undone_trades_score(self, user_id: long, reset_cache=False):
        undone_trade: UndoneTrade = UndoneTrade.objects(user_id=user_id).first()
        done_trade: DoneTrade = DoneTrade.objects(user_id=user_id).first()
        rds: RedisCachingRulesUndoneTrades = self.rds.get_redis_caching_rules_undone_trades_service(reset_cache)
        undone_trades_score = 0

        score = rds.get_score_of_rules_undone_undue_trades_counts(undone_trade.undue_trades_count)
        undone_trades_score += score
        print('score= {}, undoneTrades:[undue_trades_count]= {}'.format(score, undone_trade.undue_trades_count))

        # calculate undue_total_balance_ratio
        undue_total_balance_ratio = float(undone_trade.undue_trades_total_balance_of_last_year / done_trade.trades_total_balance)
        score = rds.get_score_of_rules_undone_undue_trades_total_balance_of_last_year_ratios(undue_total_balance_ratio)
        undone_trades_score += score
        print('score= {}, undoneTrades:[undue_total_balance_ratio]= {}'.format(score, undue_total_balance_ratio))

        score = rds.get_score_of_rules_undone_past_due_trades_counts(undone_trade.past_due_trades_count)
        undone_trades_score += score
        print('score= {}, undoneTrades:[past_due_trades_count]= {}'.format(score, undone_trade.past_due_trades_count))

        timely_done_trades_of_last_year = (
                done_trade.timely_trades_count_of_last_3_months + done_trade.timely_trades_count_between_last_3_to_12_months)
        # calculate past_due_total_balance_ratio
        past_due_total_balance_ratio = float(undone_trade.past_due_trades_total_balance_of_last_year / done_trade.trades_total_balance)
        score = rds.get_score_of_rules_undone_past_due_trades_total_balance_of_last_year_ratios(past_due_total_balance_ratio)
        score_code = rds.get_score_code_of_rules_undone_past_due_trades_total_balance_of_last_year_ratios(past_due_total_balance_ratio)
        if timely_done_trades_of_last_year == 1 and score_code == SCORE_CODE_RULES_UNDONE_PAST_DUE_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS:
            score *= 2
        undone_trades_score += score
        print('score= {}, undoneTrades:[past_due_total_balance_ratio]= {}'.format(score, past_due_total_balance_ratio))

        score = rds.get_score_of_rules_undone_arrear_trades_counts(undone_trade.arrear_trades_count)
        undone_trades_score += score
        print('score= {}, undoneTrades:[arrear_trades_count]= {}'.format(score, undone_trade.arrear_trades_count))

        # calculate arrear_total_balance_ratio
        arrear_total_balance_ratio = float(undone_trade.arrear_trades_total_balance_of_last_year / done_trade.trades_total_balance)
        score = rds.get_score_of_rules_undone_arrear_trades_total_balance_of_last_year_ratios(arrear_total_balance_ratio)
        score_code = rds.get_score_code_of_rules_undone_arrear_trades_total_balance_of_last_year_ratios(arrear_total_balance_ratio)
        if timely_done_trades_of_last_year == 1 and score_code == SCORE_CODE_RULES_UNDONE_ARREAR_TRADES_TOTAL_BALANCE_OF_LAST_YEAR_RATIOS:
            score *= 2
        undone_trades_score += score
        print('score= {}, undoneTrades:[arrear_total_balance_ratio]= {}'.format(score, arrear_total_balance_ratio))

        print('............. undoneTrades score = {} ................\n'.format(undone_trades_score))
        return undone_trades_score

    def calculate_user_loans_score(self, user_id: long, reset_cache=False):
        loan: Loan = Loan.objects(user_id=user_id).first()
        rds: RedisCachingRulesLoans = self.rds.get_redis_caching_rules_loans_service(reset_cache)
        loans_score = 0

        score = rds.get_score_of_rules_loans_total_counts(loan.loans_total_count)
        loans_score += score
        print('score= {}, loans:[loans_total_count]= {}'.format(score, loan.loans_total_count))

        # should be calculate avg_of_all_users_monthly_installment_total_balance
        avg_of_all_users_monthly_installment_total_balance = 4000000
        installments_total_balance_ratio = float(loan.monthly_installments_total_balance / avg_of_all_users_monthly_installment_total_balance)
        score = rds.get_score_of_rules_loan_monthly_installments_total_balance_ratios(installments_total_balance_ratio)
        loans_score += score
        print('score= {}, loans:[installments_total_balance_ratio]= {}'.format(score, installments_total_balance_ratio))

        # should be calculate user_total_loans_balance
        overdue_total_balance_ratio = 0 if loan.loans_total_balance == 0 else float(loan.overdue_loans_total_balance / loan.loans_total_balance)
        score = rds.get_score_of_rules_overdue_loans_total_balance_ratios(overdue_total_balance_ratio)
        loans_score += score
        print('score= {}, loans:[overdue_total_balance_ratio]= {}'.format(score, overdue_total_balance_ratio))

        score = rds.get_score_of_rules_past_due_loans_total_counts(loan.past_due_loans_total_count)
        loans_score += score
        print('score= {}, loans:[past_due_loans_total_count]= {}'.format(score, loan.past_due_loans_total_count))

        # should be calculate user_total_loans_balance
        past_due_total_balance_ratio = 0 if loan.loans_total_balance == 0 else float(loan.past_due_loans_total_balance / loan.loans_total_balance)
        score = rds.get_score_of_rules_past_due_loans_total_balance_ratios(past_due_total_balance_ratio)
        loans_score += score
        print('score= {}, loans:[past_due_total_balance_ratio]= {}'.format(score, past_due_total_balance_ratio))

        score = rds.get_score_of_rules_arrear_loans_total_counts(loan.arrear_loans_total_count)
        loans_score += score
        print('score= {}, loans:[arrear_loans_total_count]= {}'.format(score, loan.arrear_loans_total_count))

        # should be calculate user_total_loans_balance
        arrear_total_balance_ratio = 0 if loan.loans_total_balance == 0 else float(loan.arrear_loans_total_balance / loan.loans_total_balance)
        score = rds.get_score_of_rules_arrear_loans_total_balance_ratios(arrear_total_balance_ratio)
        loans_score += score
        print('score= {}, loans:[arrear_total_balance_ratio]= {}'.format(score, arrear_total_balance_ratio))

        score = rds.get_score_of_rules_suspicious_loans_total_counts(loan.suspicious_loans_total_count)
        loans_score += score
        print('score= {}, loans:[suspicious_loans_total_count]= {}'.format(score, loan.suspicious_loans_total_count))

        # should be calculate user_total_loans_balance
        suspicious_total_balance_ratio = 0 if loan.loans_total_balance == 0 else float(loan.suspicious_loans_total_balance / loan.loans_total_balance)
        score = rds.get_score_of_rules_suspicious_loans_total_balance_ratios(suspicious_total_balance_ratio)
        loans_score += score
        print('score= {}, loans:[suspicious_total_balance_ratio]= {}'.format(score, suspicious_total_balance_ratio))

        print('............. loans score = {} ................\n'.format(loans_score))
        return loans_score

    def calculate_user_cheques_score(self, user_id: long, reset_cache=False):
        cheque: Cheque = Cheque.objects(user_id=user_id).first()
        rds: RedisCachingRulesCheques = self.rds.get_redis_caching_rules_cheques_service(reset_cache)
        cheque_score = 0

        score = rds.get_score_of_rules_unfixed_returned_cheques_count_between_last_3_to_12_months(
            cheque.unfixed_returned_cheques_count_between_last_3_to_12_months)
        cheque_score += score
        print('score= {}, cheques:[unfixed_returned_cheques_count_between_last_3_to_12_months]= {}'
              .format(score, cheque.unfixed_returned_cheques_count_between_last_3_to_12_months))

        score = rds.get_score_of_rules_unfixed_returned_cheques_count_of_last_3_months(
            cheque.unfixed_returned_cheques_count_of_last_3_months)
        cheque_score += score
        print('score= {}, cheques:[unfixed_returned_cheques_count_of_last_3_months]= {}'
              .format(score, cheque.unfixed_returned_cheques_count_of_last_3_months))

        score = rds.get_score_of_rules_unfixed_returned_cheques_count_of_last_5_years(
            cheque.unfixed_returned_cheques_count_of_last_5_years)
        cheque_score += score
        print('score= {}, cheques:[unfixed_returned_cheques_count_of_last_5_years]= {}'
              .format(score, cheque.unfixed_returned_cheques_count_of_last_5_years))

        score = rds.get_score_of_rules_unfixed_returned_cheques_count_of_more_12_months(
            cheque.unfixed_returned_cheques_count_of_more_12_months)
        cheque_score += score
        print('score= {}, cheques:[unfixed_returned_cheques_count_of_more_12_months]= {}'
              .format(score, cheque.unfixed_returned_cheques_count_of_more_12_months))

        # should be calculate avg_of_all_users_unfixed_returned_cheques_total_balance
        avg_of_all_users_unfixed_returned_cheques_total_balance = 40000000000
        total_balance_ratio = float(cheque.unfixed_returned_cheques_total_balance / avg_of_all_users_unfixed_returned_cheques_total_balance)
        score = rds.get_score_of_rules_unfixed_returned_cheques_total_balance_ratios(total_balance_ratio)
        cheque_score += score
        print('score= {}, cheques:[total_balance_ratio]= {}'.format(score, total_balance_ratio))

        print('............. cheques score = {} ................\n'.format(cheque_score))
        return cheque_score
