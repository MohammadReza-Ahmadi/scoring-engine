from datetime import datetime, date
from typing import List

from pydantic import parse_obj_as
from pymongo.command_cursor import CommandCursor
from pymongo.cursor import Cursor
from pymongo.database import Database

from app.core.constants import USER_ID, DAYS, MONTHS, SCORE_DISTRIBUTION_SEPARATOR, ZERO, ONE, CODE, TIMELINESS, VOLUMES, HISTORIES, IDENTITIES, ONE_HUNDRED
from app.core.database import get_db
from app.core.exceptions import ScoringException
from app.core.models.cheques import Cheque
from app.core.models.done_trades import DoneTrade
from app.core.models.dtos.cheque_status_dto import ChequesStatusDTO
from app.core.models.dtos.loan_status_dto import LoansStatusDTO
from app.core.models.dtos.score_boundaries_dto import ScoreBoundariesDTO
from app.core.models.dtos.score_details_dto import ScoreDetailsDTO
from app.core.models.dtos.score_distribution_dto import ScoreDistributionDTO
from app.core.models.dtos.score_status_dto import ScoreStatusDTO
from app.core.models.dtos.vosouq_status_dto import VosouqStatusDTO
from app.core.models.loans import Loan
from app.core.models.profile import Profile
from app.core.models.rules import Rule
from app.core.models.score_gauges import ScoreGauge
from app.core.models.undone_trades import UndoneTrade
from app.core.services.pipelines_generator import generate_scores_distributions_pipeline
from app.core.services.util import create_score_status_dto, create_vosouq_status_dto, calculate_dates_diff, create_loan_status_dto, create_cheque_status_dto, \
    get_zero_if_null, create_score_details_dto, get_second_item
from app.core.settings import min_score, max_score, distribution_count


class DataService:
    def __init__(self, db: Database = None) -> None:
        super().__init__()
        self.db = get_db() if db is None else db

    # SCORE-GAUGE SERVICES ................................................
    def get_score_gauges(self) -> list:
        sgs = self.db.scoreGauges.find()
        return list(sgs)

    def insert_score_gauge(self, sg: ScoreGauge):
        self.db.scoreGauges.insert_one(dict(sg))

    # RULE SERVICES ........................................................
    def insert_rule(self, r: Rule):
        self.db.rules.insert_one(dict(r))

    def get_rule(self, filter_dict: {}) -> Rule:
        if filter_dict is None:
            raise ScoringException(1, 'filter_dict is empty!')
        return self.db.rules.find_one(filter_dict)

    def get_rules(self, filter_dict: {} = None) -> [Rule]:
        if filter_dict is not None:
            return self.db.rules.find(filter_dict)
        return self.db.rules.find()

    def get_master_rules(self) -> [Rule]:
        dic: Cursor = self.db.rules.find({CODE: {'$in': [IDENTITIES, HISTORIES, VOLUMES, TIMELINESS]}})
        if dic is None:
            return []
        rules: [Rule] = []
        while dic.alive:
            rules.append(Rule.parse_obj(dic.next()))
        return rules

    def delete_rules(self, filter_dict: {}) -> None:
        self.db.rules.delete_many(filter_dict)

    def get_master_rules_boundaries_dict(self):
        rules = self.get_master_rules()
        m_dict: {} = {}
        for r in rules:
            m_dict.__setitem__(r.code, [r.score, r.impact_percent])
        return m_dict

    # PROFILE SERVICES ................................................
    def insert_profile(self, p: Profile):
        if p.membership_date is not None:
            # set min time value to date filed, pydantic model does not support date without time field type
            p.membership_date = datetime.combine(p.membership_date, datetime.min.time())
        self.db.profiles.insert_one(dict(p))

    def get_profiles(self, filter_dict: {}) -> List[Profile]:
        if filter_dict is None:
            raise ScoringException(2, 'filter_dict is empty!')
        dic = self.db.profiles.find(filter_dict)
        if dic is None:
            return []
        return parse_obj_as(List[Profile], dic)

    def get_user_profile(self, user_id: int) -> Profile:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        dic = self.db.profiles.find_one({USER_ID: user_id})
        if dic is None:
            return Profile()
        return Profile.parse_obj(dic)

    def delete_profiles(self, filter_dict: {}) -> None:
        self.db.profiles.delete_many(filter_dict)

    # DONE-TRADE SERVICES ................................................
    def get_done_trades(self, filter_dict: {}) -> List[DoneTrade]:
        if filter_dict is None:
            raise ScoringException(2, 'filter_dict is empty!')
        dic = self.db.doneTrades.find(filter_dict)
        if dic is None:
            return []
        return parse_obj_as(List[DoneTrade], dic)

    def get_user_done_trade(self, user_id: int) -> DoneTrade:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        dic = self.db.doneTrades.find_one({USER_ID: user_id})
        if dic is None:
            return DoneTrade()
        return DoneTrade.parse_obj(dic)

    # UNDONE-TRADE SERVICES ................................................
    def get_undone_trades(self, filter_dict: {}) -> List[UndoneTrade]:
        if filter_dict is None:
            raise ScoringException(2, 'filter_dict is empty!')
        dic = self.db.undoneTrades.find(filter_dict)
        if dic is None:
            return []
        return parse_obj_as(List[UndoneTrade], dic)

    def get_user_undone_trade(self, user_id: int) -> UndoneTrade:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        dic = self.db.undoneTrades.find_one({USER_ID: user_id})
        if dic is None:
            return UndoneTrade()
        return UndoneTrade.parse_obj(dic)

    # LOAN SERVICES ................................................
    def get_loans(self, filter_dict: {}) -> List[Loan]:
        if filter_dict is None:
            raise ScoringException(2, 'filter_dict is empty!')
        dic = self.db.loans.find(filter_dict)
        if dic is None:
            return []
        return parse_obj_as(List[Loan], dic)

    def get_user_loan(self, user_id: int) -> Loan:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        dic = self.db.loans.find_one({USER_ID: user_id})
        if dic is None:
            return Loan()
        return Loan.parse_obj(dic)

    # CHEQUE SERVICES ................................................
    def get_cheques(self, filter_dict: {}) -> List[Cheque]:
        if filter_dict is None:
            raise ScoringException(2, 'filter_dict is empty!')
        dic = self.db.cheques.find(filter_dict)
        if dic is None:
            return []
        return parse_obj_as(List[Cheque], dic)

    def get_user_cheque(self, user_id: int) -> Cheque:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        dic = self.db.cheques.find_one({USER_ID: user_id})
        if dic is None:
            return Cheque()
        return Cheque.parse_obj(dic)

    # REST SERVICES ................................................
    def get_score_boundaries(self) -> ScoreBoundariesDTO:
        rb = self.get_master_rules_boundaries_dict()
        # calculate max scores boundaries based on max_score
        i_max_score = (max_score * get_second_item(rb.get(IDENTITIES))) // ONE_HUNDRED
        h_max_score = (max_score * get_second_item(rb.get(HISTORIES))) // ONE_HUNDRED
        v_max_score = (max_score * get_second_item(rb.get(VOLUMES))) // ONE_HUNDRED
        t_max_score = (max_score * get_second_item(rb.get(TIMELINESS))) // ONE_HUNDRED
        score_boundaries_dto = ScoreBoundariesDTO(identities_max_score=i_max_score, histories_max_score=h_max_score,
                                                  volumes_max_score=v_max_score, timeliness_max_score=t_max_score,
                                                  min_score=min_score, max_score=max_score)
        return score_boundaries_dto

    def get_score_status(self, user_id: int) -> ScoreStatusDTO:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        pf: Profile = self.get_user_profile(user_id)
        gs = self.get_score_gauges()
        return create_score_status_dto(pf.score, gs, 8, datetime.today())

    def get_vosouq_status(self, user_id: int) -> VosouqStatusDTO:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')

        # load profile
        pf: Profile = self.get_user_profile(user_id)
        if pf.membership_date is None:
            pf.membership_date = date.today()

        # calc membership duration
        membership_duration = calculate_dates_diff(
            datetime(year=pf.membership_date.year,
                     month=pf.membership_date.month,
                     day=pf.membership_date.day),
            datetime.today())

        # load & calc doneTrade
        # load doneTrade
        dt: DoneTrade = self.get_user_done_trade(user_id)
        # calc all doneTrades count
        dt_count = get_zero_if_null(dt.timely_trades_count_of_last_3_months) + get_zero_if_null(dt.timely_trades_count_between_last_3_to_12_months) \
                   + get_zero_if_null(dt.past_due_trades_count_of_last_3_months) + get_zero_if_null(dt.past_due_trades_count_between_last_3_to_12_months) \
                   + get_zero_if_null(dt.arrear_trades_count_of_last_3_months) + get_zero_if_null(dt.arrear_trades_count_between_last_3_to_12_months)
        # calc delayed doneTrades count
        delay_days_avg = 0
        if dt_count > 0:
            delayed_dt_count = dt_count - (
                    get_zero_if_null(dt.timely_trades_count_of_last_3_months) + get_zero_if_null(dt.timely_trades_count_between_last_3_to_12_months))
            # calc delayDays' avg
            delay_days_avg = dt.total_delay_days // delayed_dt_count

        # calc negativeStatus count
        # todo: this field should be calculated later based on negative_histories which should be provided
        negative_status_count = 0

        # load & calc undoneTrade
        udt: UndoneTrade = self.get_user_undone_trade(user_id)
        # calc all undoneTrades count
        udt_count = get_zero_if_null(udt.undue_trades_count) + get_zero_if_null(udt.past_due_trades_count) + get_zero_if_null(udt.arrear_trades_count)

        # make & return VosouqStatusDTO
        return create_vosouq_status_dto(membership_duration[DAYS], membership_duration[MONTHS], dt_count,
                                        udt_count, negative_status_count, delay_days_avg, pf.recommended_to_others_count)

    def get_loans_status(self, user_id: int) -> LoansStatusDTO:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        ln: Loan = self.get_user_loan(user_id)
        return create_loan_status_dto(ln)

    def get_cheques_status(self, user_id: int) -> ChequesStatusDTO:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        ch: Cheque = self.get_user_cheque(user_id)
        return create_cheque_status_dto(ch)

    def get_score_details(self, user_id: int) -> ScoreDetailsDTO:
        if user_id is None:
            raise ScoringException(3, 'user_id can not be None!')
        pf: Profile = self.get_user_profile(user_id)
        return create_score_details_dto(pf)

    def get_score_distributions(self) -> List[ScoreDistributionDTO]:
        pipeline = generate_scores_distributions_pipeline(min_score, max_score, distribution_count)
        score_distro: CommandCursor = self.db.profiles.aggregate(pipeline)
        score_distro_dict: {} = score_distro.next()
        score_distro_dtos: [ScoreDistributionDTO] = []
        for k in score_distro_dict.keys():
            score_range: [] = k.split(SCORE_DISTRIBUTION_SEPARATOR)
            score_distro_dtos.append(ScoreDistributionDTO(from_score=score_range[ZERO], to_score=score_range[ONE], count=score_distro_dict[k]))
        return score_distro_dtos
