from pydantic import BaseModel


class LoansStatusDTO(BaseModel):
    current_loans_count: int = 0
    past_due_loans_amount: int = 0
    arrears_loans_amount: int = 0
    suspicious_loans_amount: int = 0
