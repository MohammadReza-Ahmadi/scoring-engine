from numpy import long

from data.done_trades import DoneTrade
from data.profile import Profile
from src.service import general_data_service as gs


def calculate_user_final_score(user_id: long):
    print()


def calculate_user_profile_score(user_id: long):
    profile = gs.get_document_by_user_id(Profile.__name__, user_id)
    print()


def calculate_user_done_trades_score(user_id: long):
    done_trade: DoneTrade = gs.get_document_by_user_id(DoneTrade.__name__, user_id)

    # done_trade.calculation_start_date

    done_trade.timely_trades_count_of_last_3_months
    done_trade.past_due_trades_count_of_last_3_months
    done_trade.arrear_trades_count_of_last_3_months
    done_trade.timely_trades_count_between_last_3_to_12_months
    done_trade.past_due_trades_count_between_last_3_to_12_months
    done_trade.arrear_trades_count_between_last_3_to_12_months
    done_trade.trades_total_balance
    done_trade.total_delay_days


