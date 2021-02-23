from datetime import date

from pydantic import BaseModel

from app.core.models.scoring_enums import ProfileMilitaryServiceStatusEnum


class Profile(BaseModel):
    user_id: int = None
    has_kyc: bool = False
    military_service_status: ProfileMilitaryServiceStatusEnum = ProfileMilitaryServiceStatusEnum.FINISHED
    sim_card_ownership: bool = False
    address_verification: bool = False
    membership_date: date = None
    recommended_to_others_count: int = None
    number_of_times_star_received: int = None
    star_count_average: int = None
    score: int = None
    identities_score: int = None
    histories_score: int = None
    volumes_score: int = None
    timeliness_score: int = None

    # class Config:
    #     orm_mode = True

    # Profile = create_model(
    #     'BarModel',
    #     apple='russet',
    #     banana='yellow',
    #     __base__=FooModel,
    # )

