from datetime import date

from pymongo.command_cursor import CommandCursor

from app.core.database import get_db
from app.core.models.profile import Profile
from app.core.models.scoring_enums import ProfileMilitaryServiceStatusEnum
from app.core.services.pipelines_generator import generate_scores_distributions_pipeline
from app.core.services.data_service import DataService

if __name__ == '__main__':
    ds = DataService(get_db())
    range_score = 0
    for i in range(1):
        p = Profile(user_id=int(2000 + i))
        p.has_kyc = True
        p.military_service_status = ProfileMilitaryServiceStatusEnum.FINISHED
        p.sim_card_ownership = True
        p.address_verification = True
        p.membership_date = date.today()
        p.recommended_to_others_count = 23
        p.star_count_average = 1
        p.score = i
        # if i % 50 == 0:
        #     p.score = (i // 50) * 50
        # else:
        #     p.score = range_score
        # ds.insert_profile(p)
        pipeline = generate_scores_distributions_pipeline(0, 1000, 20)
        ref: CommandCursor = ds.db.profiles.aggregate(pipeline)
        # ref: CommandCursor = ds.db.profiles.aggregate(scores_distributions_pipeline)

        # print(ref[0].get('0_to_50'))
        for r in ref:
            print(r)
