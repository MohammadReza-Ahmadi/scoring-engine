import program
from data.score_gauges import ScoreGauge


def import_score_gauges():
    sg = ScoreGauge()
    sg.start = 0
    sg.end = 499
    sg.color = 'red'
    sg.label = 'خیلی ضعیف'
    sg.risk_status = 'بسیار بالا'
    sg.save()

    sg = ScoreGauge()
    sg.start = 500
    sg.end = 589
    sg.color = 'light brown'
    sg.label = 'ضعیف'
    sg.risk_status = 'بالا'
    sg.save()

    sg = ScoreGauge()
    sg.start = 590
    sg.end = 669
    sg.color = 'dark yellow'
    sg.label = 'متوسط'
    sg.risk_status = 'متوسط'
    sg.save()

    sg = ScoreGauge()
    sg.start = 670
    sg.end = 749
    sg.color = 'light green'
    sg.label = 'خوب'
    sg.risk_status = 'پایین'
    sg.save()

    sg = ScoreGauge()
    sg.start = 750
    sg.end = 1000
    sg.color = 'red'
    sg.label = 'خیلی ضعیف'
    sg.risk_status = 'بسیار بالا'
    sg.save()


if __name__ == '__main__':
    program.launch_app()
    import_score_gauges()
