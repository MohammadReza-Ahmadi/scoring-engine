import mongoengine

from src.data.rule.rule_model import RuleModel


# تعداد تسهیلات معوق در جریان
class RuleArrearLoansTotalCount(mongoengine.Document, RuleModel):
    meta = {
        'db_alias': 'core',
        'collection': 'rulesLoanArrearTotalCounts'
    }
