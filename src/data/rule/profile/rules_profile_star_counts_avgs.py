import mongoengine

from data.rule.rule_model import RuleModel


class RuleProfileStarCountAvg(mongoengine.Document, RuleModel):
    min = mongoengine.FloatField()
    max = mongoengine.FloatField()
    meta = {
        'db_alias': 'core',
        'collection': 'rulesProfileStarCountsAvgs'
    }
