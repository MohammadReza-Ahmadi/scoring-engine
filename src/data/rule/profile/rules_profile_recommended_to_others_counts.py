import mongoengine

from data.rule.rule_model import RuleModel


class RuleProfileRecommendedToOthersCount(mongoengine.Document, RuleModel):
    meta = {
        'db_alias': 'core',
        'collection': 'rulesProfileRecommendedToOthersCounts'
    }
