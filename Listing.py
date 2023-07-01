# Listing class
class Listing:
    count_id = 0

    # initializer method
    def __init__(self, listing_owner, listing_name, listing_price, listing_description, listing_stock, listing_location):
        Listing.count_id += 1
        self.__listing_id = Listing.count_id
        self.__listing_owner = listing_owner
        self.__listing_name = listing_name
        self.__listing_price = listing_price
        self.__listing_description = listing_description
        self.__listing_stock = listing_stock
        self.__listing_location = listing_location

    # accessor methods
    def get_listing_id(self):
        return self.__listing_id

    def get_listing_owner(self):
        return self.__listing_owner

    def get_listing_name(self):
        return self.__listing_name

    def get_listing_price(self):
        return self.__listing_price

    def get_listing_description(self):
        return self.__listing_description

    def get_listing_stock(self):
        return self.__listing_stock
    
    def get_listing_location(self):
        return self.__listing_location

    # mutator methods
    def set_listing_id(self, listing_id):
        self.__listing_id = listing_id

    def set_listing_owner(self, listing_owner):
        self.__listing_owner = listing_owner

    def set_listing_name(self, listing_name):
        self.__listing_name = listing_name

    def set_listing_price(self, listing_price):
        self.__listing_price = listing_price

    def set_listing_description(self, listing_description):
        self.__listing_description = listing_description

    def set_listing_stock(self, listing_stock):
        self.__listing_stock = listing_stock

    def set_listing_location(self, listing_location):
        self.__listing_location = listing_location