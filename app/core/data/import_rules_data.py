from app.core.data.import_history_rules_data import import_rules_histories
from app.core.data.import_identity_rules_data import import_rules_identities
from app.core.data.import_score_gauges_data import import_score_gauges
from app.core.data.import_timeliness_rules_data import import_rules_timeliness
from app.core.data.import_volume_rules_data import import_rules_volumes
from app.core.database import get_db
from app.core.services.data_service import DataService


def import_rules(ds: DataService):
    import_score_gauges(ds)
    import_rules_identities(ds)
    import_rules_histories(ds)
    import_rules_volumes(ds)
    import_rules_timeliness(ds)


if __name__ == '__main__':
    import_rules(DataService(get_db()))
