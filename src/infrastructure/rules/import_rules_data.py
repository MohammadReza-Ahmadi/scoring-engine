from infrastructure.rules.import_history_rules_data import import_rules_histories
from infrastructure.rules.import_identity_rules_data import import_rules_identities
from infrastructure.rules.import_timeliness_rules_data import import_rules_timeliness
from infrastructure.rules.import_volume_rules_data import import_rules_volumes

if __name__ == '__main__':
    import_rules_identities()
    import_rules_histories()
    import_rules_volumes()
    import_rules_timeliness()
