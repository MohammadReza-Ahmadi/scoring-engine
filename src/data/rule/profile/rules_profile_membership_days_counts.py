import mongoengine

from data.rule.rule_model import RuleModel


class RuleProfileMembershipDaysCount(mongoengine.Document, RuleModel):
    meta = {
        'db_alias': 'core',
        'collection': 'rulesProfileMembershipDaysCounts'
    }
