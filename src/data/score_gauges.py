import mongoengine


class ScoreGauge(mongoengine.Document):
    start = mongoengine.IntField()
    end = mongoengine.IntField()
    color = mongoengine.StringField()
    label = mongoengine.StringField()
    risk_status = mongoengine.StringField()

    meta = {
        'db_alias': 'core',
        'collection': 'scoreGauges'
    }