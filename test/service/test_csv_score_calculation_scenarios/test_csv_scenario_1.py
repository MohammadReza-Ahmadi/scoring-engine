import csv
from datetime import date, timedelta

import program
from data.cheques import Cheque
from data.done_trades import DoneTrade
from data.loans import Loan
from data.profile import Profile
from data.undone_trades import UndoneTrade
from infrastructure.caching.redis_caching import RedisCaching
from infrastructure.constants import AVG_OF_ALL_USERS_UNFIXED_RETURNED_CHEQUES_TOTAL_BALANCE
from infrastructure.scoring_enums import ProfileMilitaryServiceStatusEnum
from service.score_calculation_service import ScoreCalculationService


def read_scenarios_dicts_from_csv(csv_path):
    scenarios_dicts = []
    with open(csv_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # col_values = ', '.join(row).split(',')
            if line_count == 0:
                print(f'Column names are:\n {", ".join(row)}')
            line_count += 1
            scenarios_dicts.append(row)
        print(f'Processed {line_count} lines.')
    return scenarios_dicts


def calculate_score(scenarios_dicts: []):
    program.launch_app()
    rds = RedisCaching()
    cs = ScoreCalculationService(rds)

    for scn_dict in scenarios_dicts:
        expected_score = scn_dict['Vscore']

        p = Profile()
        p.has_kyc = scn_dict['KYC']
        p.military_service_status = ProfileMilitaryServiceStatusEnum.__getitem__(scn_dict['Military'])
        p.sim_card_ownership = scn_dict['SimCard']
        p.address_verification = scn_dict['Address']
        p.membership_date = date.today() - timedelta(days=int(scn_dict['Membership']))
        p.recommended_to_others_count = scn_dict['Recommendation']
        p.star_count_average = scn_dict['WeightedAveStars']
        profile_score = cs.calculate_user_profile_score(user_id=0, profile_object=p)

        dt = DoneTrade()
        dt.timely_trades_count_of_last_3_months = scn_dict['Last3MSD']
        dt.timely_trades_count_between_last_3_to_12_months = scn_dict['Last1YSD']
        dt.past_due_trades_count_of_last_3_months = scn_dict['B30DayDelayLast3M']
        dt.past_due_trades_count_between_last_3_to_12_months = scn_dict['B30DayDelayLast3-12M']
        dt.arrear_trades_count_of_last_3_months = scn_dict['A30DayDelayLast3M']
        dt.arrear_trades_count_between_last_3_to_12_months = scn_dict['A30DayDelay3-12M']
        dt.total_delay_days = scn_dict['AverageDelayRatio']
        # todo: 100000000 is fix Denominator that is all_other_users_done_trades_amount, it should be change later
        dt.trades_total_balance = round(float(scn_dict['SDealAmountRatio']) * 100000000)
        done_trades_score = cs.calculate_user_done_trades_score(user_id=0, done_trade_object=dt)

        udt = UndoneTrade()
        udt.undue_trades_count = scn_dict['NumNotDueDeal']
        udt.past_due_trades_count = scn_dict['UnfinishedB30DayDelay']
        udt.arrear_trades_count = scn_dict['UnfinishedA30DayDelay']
        udt.undue_trades_total_balance_of_last_year = round(float(scn_dict['NotDueDealAmountRatio']) * dt.trades_total_balance)
        udt.past_due_trades_total_balance_of_last_year = round(float(scn_dict['UnfinishedB30Din1YRatio']) * dt.trades_total_balance)
        udt.arrear_trades_total_balance_of_last_year = round(float(scn_dict['UnfinishedA30Din1YRatio']) * dt.trades_total_balance)
        undone_trades_score = cs.calculate_user_undone_trades_score(user_id=0, undone_trade_object=udt, done_trade_object=dt)

        ln = Loan()
        ln.loans_total_count = scn_dict['Loans']
        ln.loans_total_balance = 70000000
        ln.past_due_loans_total_count = int(scn_dict['PastDueLoans'])
        ln.arrear_loans_total_count = int(scn_dict['DelayedLoans'])
        ln.suspicious_loans_total_count = int(scn_dict['DoubfulCollectionLoans'])
        ln.monthly_installments_total_balance = float(scn_dict['MonthlyInstallments'])
        ln.overdue_loans_total_balance = round(float(scn_dict['CurrentLoanAmountRatio']) * ln.loans_total_balance)
        ln.past_due_loans_total_balance = round(float(scn_dict['PastDueLoanAmountRatio']) * ln.loans_total_balance)
        ln.arrear_loans_total_balance = round(float(scn_dict['DelayedLoanAmountRatio']) * ln.loans_total_balance)
        ln.suspicious_loans_total_balance = round(float(scn_dict['DoubtfulCollectionAmountRatio']) * ln.loans_total_balance)
        loan_score = cs.calculate_user_loans_score(user_id=0, loan_object=ln)

        ch = Cheque()
        ch.unfixed_returned_cheques_count_of_last_3_months = scn_dict['DishonouredChequesL3M']
        ch.unfixed_returned_cheques_count_between_last_3_to_12_months = scn_dict['DishonouredChequesL3-12M']
        ch.unfixed_returned_cheques_count_of_more_12_months = scn_dict['DishonouredChequesA12M']
        ch.unfixed_returned_cheques_count_of_last_5_years = scn_dict['AllDishonouredCheques']
        ch.unfixed_returned_cheques_total_balance = round(float(scn_dict['DCAmountRatio']) * AVG_OF_ALL_USERS_UNFIXED_RETURNED_CHEQUES_TOTAL_BALANCE)
        cheque_score = cs.calculate_user_cheques_score(user_id=0, cheque_object=ch)

        final_score = profile_score + done_trades_score + undone_trades_score + loan_score + cheque_score
        print('<><><><><><><> expected-score= {} and final-score = {} <><><><><><><>'.format(expected_score, final_score))


if __name__ == '__main__':
    csv_file_path = '/home/vsq-docs-live/scoring/_@RISK-Files/Vscore-sample-scenario.csv'
    sd = read_scenarios_dicts_from_csv(csv_file_path)
    calculate_score(sd)
