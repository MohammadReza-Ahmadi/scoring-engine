import mongoengine

from data.rule.rule_model import RuleModel


class RuleProfileSimCardOwnership(mongoengine.Document, RuleModel):
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        delattr(self, 'min')
        delattr(self, 'max')

    status_code = mongoengine.IntField()
    meta = {
        'db_alias': 'core',
        'collection': 'rulesProfileSimCardOwnerships'
    }
