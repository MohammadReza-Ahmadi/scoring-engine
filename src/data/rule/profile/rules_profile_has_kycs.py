import mongoengine

from data.rule.rule_model import RuleModel


class RuleProfileHasKyc(mongoengine.Document, RuleModel):
    def __init__(self, *args, **values):
        super().__init__(*args, **values)
        delattr(self, 'min')
        delattr(self, 'max')

    status_code = mongoengine.IntField()
    # status = mongoengine.BooleanField()
    # military_service_status = mongoengine.EnumField(ProfileMilitaryServiceStatusEnum)

    meta = {
        'db_alias': 'core',
        'collection': 'rulesProfileHasKycs'
    }
