class Customer():
    count_id = 0

    def __init__(self, first_name, last_name, gender, email, date_joined, address, membership, remarks, status = 'Available', sessionid = 0):

        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__email = email
        self.__date_joined = date_joined
        self.__address = address
        self.__status = status
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__membership = membership
        self.__remarks = remarks
        self.__sessionid = sessionid
    # accessor methods

    def get_sessionid(self):
        return self.__sessionid

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_membership(self):
        return self.__membership

    def get_remarks(self):
        return self.__remarks

    def get_customer_id(self):
        return self.__customer_id

    def get_email(self):
        return self.__email

    def get_date_joined(self):
        return self.__date_joined

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status

    # mutator methods

    def set_sessionid(self, sessionid):
        self.__sessionid = sessionid

    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined

    def set_status(self, status):
        self.__status = status

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_membership(self, membership):
        self.__membership = membership

    def set_remarks(self, remarks):
        self.__remarks = remarks
