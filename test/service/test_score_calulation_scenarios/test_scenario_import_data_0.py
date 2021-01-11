from _datetime import datetime

from numpy import long

import program
from data.cheques import Cheque
from data.done_trades import DoneTrade
from data.loans import Loan
from data.profile import Profile
from data.undone_trades import UndoneTrade
from infrastructure.scoring_enums import ProfileMilitaryServiceStatusEnum
from src.service import general_data_service as gs


def import_profile_data(uid: long):
    p = Profile()
    p.drop_collection()
    p.user_id = uid
    p.has_kyc = True
    p.military_service_status = ProfileMilitaryServiceStatusEnum.FINISHED
    p.sim_card_ownership = True
    p.address_verification = True
    p.membership_date = datetime.now()
    p.recommended_to_others_count = 3
    p.star_count_average = 2
    p.score = 0
    gs.save_document(p)


def import_done_trades_data(uid: long):
    dt = DoneTrade()
    dt.drop_collection()

    dt.user_id = uid
    dt.calculation_start_date = datetime.now()
    dt.timely_trades_count_of_last_3_months = 1
    dt.past_due_trades_count_of_last_3_months = 0
    dt.arrear_trades_count_of_last_3_months = 0
    dt.timely_trades_count_between_last_3_to_12_months = 0
    dt.past_due_trades_count_between_last_3_to_12_months = 0
    dt.arrear_trades_count_between_last_3_to_12_months = 0
    dt.trades_total_balance = 1000000000.0
    dt.total_delay_days = 0
    dt.save()


def import_undone_trades_data(uid: long):
    dt = UndoneTrade()
    dt.drop_collection()

    dt.user_id = uid
    dt.calculation_start_date = datetime.now()
    dt.calculation_start_date = datetime.now()
    dt.undue_trades_count = 2
    dt.past_due_trades_count = 2
    dt.arrear_trades_count = 3
    dt.undue_trades_total_balance_of_last_year = 3000000000
    dt.past_due_trades_total_balance_of_last_year = 2000000000
    dt.arrear_trades_total_balance_of_last_year = 10000000
    dt.save()


def import_cheque_data(uid: long):
    ch = Cheque()
    ch.drop_collection()
    ch.user_id = uid
    ch.unfixed_returned_cheques_count_of_last_3_months = 0
    ch.unfixed_returned_cheques_count_between_last_3_to_12_months = 0
    ch.unfixed_returned_cheques_count_of_more_12_months = 0
    ch.unfixed_returned_cheques_count_of_last_5_years = 0
    ch.unfixed_returned_cheques_total_balance = 0
    ch.save()


def import_loan_data(uid: long):
    ln = Loan()
    ln.drop_collection()
    ln.user_id = uid
    ln.loans_total_count = 0
    ln.loans_total_balance = 15000000
    ln.past_due_loans_total_count = 0
    ln.arrear_loans_total_count = 0
    ln.suspicious_loans_total_count = 0
    ln.monthly_installments_total_balance = 0
    ln.overdue_loans_total_balance = 0
    ln.past_due_loans_total_balance = 0
    ln.arrear_loans_total_balance = 0
    ln.suspicious_loans_total_balance = 0
    ln.save()


if __name__ == '__main__':
    program.launch_app()
    uid = 23
    import_profile_data(uid)
    import_done_trades_data(uid)
    import_undone_trades_data(uid)
    import_cheque_data(uid)
    import_loan_data(uid)
