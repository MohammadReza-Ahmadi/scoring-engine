from app.core.database import get_db
from app.core.models.score_gauges import ScoreGauge
from app.core.services.data_service import DataService


def import_score_gauges(ds: DataService):
    # ds.db.get_collection('scoreGauges').remove()
    ds.db.scoreGauges.delete_many({})
    sg = ScoreGauge()
    sg.start = 0
    sg.end = 499
    sg.title = 'خیلی ضعیف'
    sg.color = 'fe3030'
    sg.risk_status = 'بسیار بالا'
    ds.insert_score_gauge(sg)

    sg = ScoreGauge()
    sg.start = 500
    sg.end = 589
    sg.title = 'ضعیف'
    sg.color = 'ff6800'
    sg.risk_status = 'بالا'
    ds.insert_score_gauge(sg)

    sg = ScoreGauge()
    sg.start = 590
    sg.end = 669
    sg.title = 'متوسط'
    sg.color = 'ffbb5e'
    sg.risk_status = 'متوسط'
    ds.insert_score_gauge(sg)

    sg = ScoreGauge()
    sg.start = 670
    sg.end = 749
    sg.title = 'خوب'
    sg.color = 'a6d94c'
    sg.risk_status = 'پایین'
    ds.insert_score_gauge(sg)

    sg = ScoreGauge()
    sg.start = 750
    sg.end = 1000
    sg.title = 'عالی'
    sg.color = '00d184'
    sg.risk_status = 'بسیار پایین'
    ds.insert_score_gauge(sg)


if __name__ == '__main__':
    import_score_gauges(DataService(get_db()))
