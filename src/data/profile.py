import mongoengine

from infrastructure.scoring_enums import ProfileMilitaryServiceStatusEnum


class Profile(mongoengine.Document):
    user_id = mongoengine.LongField()
    has_kyc = mongoengine.BooleanField()
    military_service_status = mongoengine.EnumField(ProfileMilitaryServiceStatusEnum)
    sim_card_ownership = mongoengine.BooleanField()
    address_verification = mongoengine.BooleanField()
    membership_date = mongoengine.DateField()
    recommended_to_others_count = mongoengine.IntField()
    number_of_times_star_received = mongoengine.IntField()
    star_count_average = mongoengine.IntField()
    score = mongoengine.IntField()

    meta = {
        'db_alias': 'core',
        'collection': 'profiles'
    }
