# RewardsBR class
class RewardsBR:
    count_id = 0

    # initializer method
    def __init__(self, status, coupon_name, rewardType, issueDate, expiryDate, description, code):
        RewardsBR.count_id += 1
        self.__rewardID = RewardsBR.count_id
        self.__status = status
        self.__couponName = coupon_name
        self.__rewardType = rewardType
        self.__issueDate = issueDate
        self.__expiryDate = expiryDate
        self.__desc = description
        self.__code = code

    # accessor methods
    def get_rewardID(self):
        return self.__rewardID

    def get_status(self):
        return self.__status

    def get_cName(self):
        return self.__couponName

    def get_rType(self):
        return self.__rewardType

    def get_issueD(self):
        return self.__issueDate

    def get_expiryD(self):
        return self.__expiryDate

    def get_desc(self):
        return self.__desc

    def get_code(self):
        return self.__code

    # mutator methods
    def set_rewardID(self, rID):
        self.__rewardID = rID

    def set_status(self, status):
        self.__status = status

    def set_couponName(self, cName):
        self.__couponName = cName

    def set_rType(self, rType):
        self.__rewardType = rType

    def set_issueD(self, issuD):
        self.__issueDate = issuD

    def set_expiryD(self, expD):
        self.__expiryDate = expD

    def set_desc(self, remarks):
        self.__desc = remarks

    def set_code(self, code):
        self.__code = code
