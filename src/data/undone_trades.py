import mongoengine


class UndoneTrade(mongoengine.Document):
    user_id = mongoengine.LongField()
    calculation_start_date = mongoengine.DateField()

    undue_trades_count = mongoengine.IntField()
    past_due_trades_count = mongoengine.IntField()
    arrear_trades_count = mongoengine.IntField()

    undue_trades_total_balance_of_last_year = mongoengine.DecimalField()
    past_due_trades_total_balance_of_last_year = mongoengine.DecimalField()
    arrear_trades_total_balance_of_last_year = mongoengine.DecimalField()

    meta = {
        'db_alias': 'core',
        'collection': 'undoneTrades'
    }
