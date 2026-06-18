from pydantic import BaseModel, Field

class Applicant(BaseModel):
    #standard Data model expects
    RevolvingUtilizationOfUnsecuredLines:   float = Field(ge=0,  description="Total balance / credit limit on cards")
    age:                                    int   = Field(ge=18, le=110, description="Age in years")
    NumberOfTime30_59DaysPastDueNotWorse:   int   = Field(ge=0,  description="Times 30-59 days late in last 2 years")
    DebtRatio:                              float = Field(ge=0,  description="Monthly debt / monthly income")
    MonthlyIncome:                          float | None = None   # nullable — some applicants didn't provide this
    NumberOfOpenCreditLinesAndLoans:        int   = Field(ge=0)
    NumberOfTimes90DaysLate:                int   = Field(ge=0)
    NumberRealEstateLoansOrLines:           int   = Field(ge=0)
    NumberOfTime60_89DaysPastDueNotWorse:   int   = Field(ge=0)
    NumberOfDependents:                     float | None = None   # nullable