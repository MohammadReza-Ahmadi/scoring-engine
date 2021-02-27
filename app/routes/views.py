# from dependency_injector.wiring import inject
from typing import List

from fastapi import APIRouter

from app.core.data.caching.redis_caching import RedisCaching
from app.core.models.dtos.cheque_status_dto import ChequesStatusDTO
from app.core.models.dtos.loan_status_dto import LoansStatusDTO
from app.core.models.dtos.score_boundaries_dto import ScoreBoundariesDTO
from app.core.models.dtos.score_changes_dto import ScoreChangesDTO
from app.core.models.dtos.score_details_dto import ScoreDetailsDTO
from app.core.models.dtos.score_distribution_dto import ScoreDistributionDTO
from app.core.models.dtos.score_status_dto import ScoreStatusDTO
from app.core.models.dtos.vosouq_status_dto import VosouqStatusDTO
from app.core.models.score_gauges import ScoreGauge
from app.core.services.data_service import DataService
from app.core.settings import redis_reset

router = APIRouter()
ds = DataService()
if bool(redis_reset):
    RedisCaching(ds).cache_rules()


# @router.get("/score-gauges", response_model=List[ScoreGauge])
@router.get("/score-gauges", response_model=List[ScoreGauge], responses={200: {"model": ScoreGauge}})
async def get_score_gauges():
    return ds.get_score_gauges()


@router.get("/score-boundaries", response_model=ScoreBoundariesDTO)
async def get_score_boundaries():
    return ds.get_score_boundaries()


# noinspection PyPep8Naming
@router.get("/score-status/{userId}", response_model=ScoreStatusDTO)
async def get_score_status(userId: int):
    return ds.get_score_status(user_id=userId)


# noinspection PyPep8Naming
@router.get("/vosouq-status/{userId}", response_model=VosouqStatusDTO)
async def get_vosouq_status(userId: int):
    return ds.get_vosouq_status(user_id=userId)


# noinspection PyPep8Naming
@router.get("/loans-status/{userId}", response_model=LoansStatusDTO)
async def get_loans_status(userId: int):
    return ds.get_loans_status(user_id=userId)


# noinspection PyPep8Naming
@router.get("/cheques-status/{userId}", response_model=ChequesStatusDTO)
async def get_cheques_status(userId: int):
    return ds.get_cheques_status(user_id=userId)


# noinspection PyPep8Naming
@router.get("/score-details/{userId}", response_model=ScoreDetailsDTO)
async def get_score_details(userId: int):
    return ds.get_score_details(user_id=userId)


# noinspection PyPep8Naming
@router.get("/score-distributions", response_model=List[ScoreDistributionDTO])
async def get_score_distribution():
    return ds.get_score_distributions()


# noinspection PyPep8Naming
@router.get("/score-changes/{userId}", response_model=List[ScoreChangesDTO])
async def get_score_distribution(userId: int):
    return ds.get_score_changes(userId)


# Just Test, should be removed
if __name__ == '__main__':
    import pandas as pd

    # data = {'Product': ['Box', 'Bottles', 'Pen', 'Markers', 'Bottles', 'Pen', 'Markers', 'Bottles', 'Box', 'Markers', 'Markers', 'Pen'],
    #         'State': ['Alaska', 'California', 'Texas', 'North Carolina', 'California', 'Texas', 'Alaska', 'Texas', 'North Carolina', 'Alaska', 'California',
    #                   'Texas'],
    #         # 'Sales': [14, 24, 31, 12, 13, 7, 9, 31, 18, 16, 18, 14]}
    #         'Sales': [14, 24, 31, 12, 13, 7, 9, 31, 18, 16, 18, 14]
    #         }
    # df1 = pd.DataFrame(data, columns=['Product', 'State', 'Sales'])
    # print(df1)

    data = {'Col1': ['v1', 'v2', 'v1'],
            'Col2': ['c1', 'c2', 'c1'],
            'Col3': [1, 1, 1]
            }
    df1 = pd.DataFrame(data, columns=['Col1', 'Col2', 'Col3'])
    r = df1.Col1.value_counts()
    print(r)
    # print(df1)
