from pydantic import BaseModel


class ChequesStatusDTO(BaseModel):
    unfixed_returned_cheques_count_of_last_3_months: int = 0
    unfixed_returned_cheques_count_between_last_3_to_12_months: int = 0
    unfixed_returned_cheques_count_of_more_12_months: int = 0
    unfixed_returned_cheques_count_of_last_5_years: int = 0

    unfixed_returned_cheques_total_balance: float = 0
