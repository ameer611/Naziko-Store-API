from pydantic import BaseModel, Field

class VerificationSentCode(BaseModel):
    phone_number: str = Field(..., min_length=9, max_length=15, example="+998901234567")
    code: int = Field(..., ge=100000, le=999999, example=123456)
    new_password: str = Field(..., min_length=6, max_length=255, example="NewPassword123")
