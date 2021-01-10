import unittest

import program
from infrastructure.caching.redis_caching import RedisCaching
from service.score_calculation_service import ScoreCalculationService


class TestScoreCalculationService(unittest.TestCase):
    # uid = 23
    uid = 1

    # FINAL SCORE CALCULATION #
    def test_calculate_final_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_final_score(self.uid)

    def test_calculate_user_profile_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_profile_score(self.uid)

    def test_calculate_user_done_trades_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_done_trades_score(self.uid)

    def test_calculate_user_undone_trades_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_undone_trades_score(self.uid)

    def test_calculate_user_loans_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_loans_score(self.uid)

    def test_calculate_user_cheques_score(self):
        program.launch_app()
        rds = RedisCaching()
        cs = ScoreCalculationService(rds)
        cs.calculate_user_cheques_score(self.uid)


if __name__ == '__main__':
    unittest.main()
