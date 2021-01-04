from data.done_trades import DoneTrade
from service.util import get_random_digits_str


def test_import_done_trades_data_11(self):
    DoneTrade.drop_collection()
    for i in range(1):
        dt = DoneTrade()
        dt.user_id = 1
        dt.timely_trades_count_of_last_3_months = get_random_digits_str(2)
        dt.timely_trades_count_between_last_3_to_12_months = get_random_digits_str(2)
        dt.past_due_trades_count_of_last_3_months = get_random_digits_str(2)
        dt.past_due_trades_count_between_last_3_to_12_months = get_random_digits_str(2)
        dt.arrear_trades_count_of_last_3_months = get_random_digits_str(2)
        dt.arrear_trades_count_between_last_3_to_12_months = get_random_digits_str(2)
        dt.trades_total_balance = get_random_digits_str(9)
        dt.total_delay_days = get_random_digits_str(2)
        gs.save_document(dt)
        print("flowing document is saved: ", dt.to_json())
