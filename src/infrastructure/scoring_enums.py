import enum


class ProfileMilitaryServiceStatusEnum(enum.Enum):
    FINISHED = 1    # پایان خدمت
    EXEMPTED = 2    # معافیت
    ONGOING = 3     # درحال خدمت
    SUBJECTED = 4   # مشمول غیر غایب
    ABSENT = 5      # غایب
