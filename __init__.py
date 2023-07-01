from datetime import datetime, date, timedelta
import calendar
from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateUserForm, CreateCustomerForm, UpdateRewardBR1
from RewardFormC import CreateRewardBR, CreateRewardBOX, UpdateRewardBR, LoginForm
import shelve, User, Customer, RewardsBR
import webbrowser


app = Flask(__name__)
staff = 'me'
customer = 'User'
app.secret_key = "ToyOutpostStaff@est2000"

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/contactUs')
def contactUs():
    return render_template('contactUs.html')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/createRewardBR', methods=['GET', 'POST'])
def create_rewardBR():
    createRewardBR = CreateRewardBR(request.form)
    if request.method == 'POST' and createRewardBR.validate():
        rewardBR_dict = {}
        db = shelve.open('rewardBR.db', 'c')

        try:
            rewardBR_dict = db['rewardBR']
        except:
            print("Error in retrieving rewards from rewardBR.db.")

        rewardsBR = RewardsBR.RewardsBR('Active', createRewardBR.coupon_name.data, createRewardBR.rType.data,
                                        createRewardBR.issueDate.data, createRewardBR.expiryDate.data,
                                        createRewardBR.description.data, createRewardBR.code.data)
        rewardBR_dict[rewardsBR.get_rewardID()] = rewardsBR
        db['rewardBR'] = rewardBR_dict

        db.close()

        return redirect(url_for('retrieve_rewardBR'))
    return render_template('createRewardBR.html', form=createRewardBR)


@app.route('/retrieveRewardBR')
def retrieve_rewardBR():
    rewardBR_dict = {}
    db = shelve.open('rewardBR.db', 'w')
    rewardBR_dict = db['rewardBR']

    rewards_list = []
    for key in rewardBR_dict:
        reward = rewardBR_dict.get(key)
        if reward.get_expiryD() <= date.today():
            reward.set_status('Expired')
            rewards_list.append(reward)
        else:
            rewards_list.append(reward)

    RewardsBR.RewardsBR.count_id = len(rewards_list)

    db['rewardBR'] = rewardBR_dict
    db.close()


    return render_template('retrieveRewardBR.html', count=len(rewards_list), rewards_list=rewards_list)


@app.route('/updateRewardBR/<int:id>/', methods=['GET', 'POST'])
def update_rewardBR(id):  ##need to do update form & recode this
    update_rewardBR = UpdateRewardBR(request.form)
    if request.method == 'POST' and update_rewardBR.validate():
        rewardBR_dict = {}
        db = shelve.open('rewardBR.db', 'w')
        rewardBR_dict = db['rewardBR']

        reward = rewardBR_dict.get(id)
        reward.set_status(update_rewardBR.status.data)
        reward.set_couponName(update_rewardBR.coupon_name.data)
        reward.set_rType(update_rewardBR.rType.data)
        reward.set_issueD(update_rewardBR.issueDate.data)
        reward.set_expiryD(update_rewardBR.expiryDate.data)
        reward.set_code(update_rewardBR.code.data)
        reward.set_desc(update_rewardBR.description.data)

        db['rewardBR'] = rewardBR_dict
        db.close()

        return redirect(url_for('retrieve_rewardBR'))
    else:
        rewardBR_dict = {}
        db = shelve.open('rewardBR.db', 'r')
        rewardBR_dict = db['rewardBR']
        db.close()

        reward = rewardBR_dict.get(id)
        update_rewardBR.status.data = reward.get_status()
        update_rewardBR.coupon_name.data = reward.get_cName()
        update_rewardBR.rType.data = reward.get_rType()
        update_rewardBR.issueDate.data = reward.get_issueD()
        update_rewardBR.expiryDate.data = reward.get_expiryD()
        update_rewardBR.code.data = reward.get_code()
        update_rewardBR.description.data = reward.get_desc()

        return render_template('updateRewardBR.html', form=update_rewardBR)


@app.route('/deleteRewardBR/<int:id>/', methods=['POST'])
def delete_rewardBR(id):
    rewardBR_dict = {}
    db = shelve.open('rewardBR.db', 'w')
    rewardBR_dict = db['rewardBR']

    rewardBR_dict.pop(id)

    db['rewardBR'] = rewardBR_dict
    db.close()

    return redirect(url_for('retrieve_rewardBR'))


@app.route('/vrewardsBOX')
def vrewardsBOX():
    currPoint = 43
    progress = (currPoint / 160) * 100
    if progress >= 100:
        progress = 100
    rewardBR_dict = {}
    db = shelve.open('rewardBR.db', 'r')
    rewardBR_dict = db['rewardBR']
    db.close()

    rewards_list = []
    for key in rewardBR_dict:
        reward = rewardBR_dict.get(key)
        rewards_list.append(reward)

    return render_template('vrewardsBOX.html', progress=progress, rewards_list=rewards_list)  # view Rewards for box`


@app.route('/vrewardsBR')
def vrewardsBR():
    if 'login' in session:
        if session['login'] == customer:
            currPoint = 69
            progress = (currPoint / 160) * 100
            if progress >= 100:
                progress = 100

            userID = session['id']
            dbc = shelve.open('rewardBR.db', 'r')
            db = shelve.open('test.db', 'r')
            rewardBR_dict = dbc['rewardBR']
            redeemedBR_list = db[userID]
            dbc.close()
            db.close()

            print(redeemedBR_list)

            rewards_list = []
            for key in rewardBR_dict:
                reward = rewardBR_dict.get(key)
                if len(redeemedBR_list) != 0:
                    for i in redeemedBR_list:
                        if int(i) == int(reward.get_rewardID()):
                            reward.set_status('Redeemed')
                            rewards_list.append(reward)
                        else:
                            rewards_list.append(reward)
                else:
                    rewards_list.append(reward)


            return render_template('vrewardsBR.html', progress=progress, rewards_list=rewards_list, count=len(rewards_list))  # view Rewards for buyer

    else:
        return redirect(url_for('login'))


@app.route('/homeStaff')
def homeStaff():
    return render_template('homeStaff.html')


@app.route('/vrewardsBR/<int:id>/', methods=['GET', 'POST'])
def redeemReward(id):
    if 'login' in session:
        if session['login'] == customer:

            rewardBR_list = []
            userID = session['id']
            dbc = shelve.open('rewardBR.db', 'r')
            db = shelve.open('test.db', 'w')
            rewardBR_dict = dbc['rewardBR']
            rewardBR_list = db[userID]
            dbc.close()

            reward = rewardBR_dict.get(id)
            rewardID = reward.get_rewardID()
            rewardBR_list.append(rewardID)

            db[userID] = rewardBR_list
            db.close()

            return redirect(url_for('vrewardsBR'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        if login_form.user_name.data == customer:
            session['login'] = login_form.user_name.data
            session['id'] = '1'


            userID = session['id']
            db = shelve.open('rewardBR.db', 'r')
            rewardBR_dict = db['rewardBR']
            db.close()

            dbC = shelve.open('test.db', 'c', writeback=True)  # open with writeback=True
            if userID in dbC:
                dbC.close()
                return render_template('welcome.html')
            else:
                list = []
                dbC[userID] = list
                dbC.close()
                return render_template('welcome.html')

        elif login_form.user_name.data == staff:
            session['login'] = login_form.user_name.data
            return redirect(url_for('homeStaff'))

    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))

@app.route('/createRewardBR1', methods=['GET', 'POST'])
def create_rewardBR1():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')
        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.email.data,
                                     create_customer_form.date_joined.data, create_customer_form.address.data, create_customer_form.membership.data, create_customer_form.remarks.data)
        ##        customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()
    return render_template('createrewardBR1.html', form=create_customer_form)

@app.route('/retrieveRewardBR1')
def retrieve_rewardBR1():
    rewardBR_dict = {}
    db = shelve.open('customer.db', 'w')
    rewardBR_dict = db['Customers']
    onedaybefore = datetime.now().date() - timedelta(days=1)

    rewards_list = []
    for key in rewardBR_dict:
        reward = rewardBR_dict.get(key)
        if reward.get_date_joined() <= date.today():
            reward.set_first_name('Enter your First Name')
            reward.set_last_name('Enter your Last Name')
            reward.set_gender('M')
            reward.set_email('example@email.com')
            reward.set_date_joined(date.today())
            reward.set_membership('D')
            reward.set_status('Available')
            reward.set_sessionid('0')
            rewards_list.append(reward)
        else:
            rewards_list.append(reward)

    Customer.Customer.count_id = len(rewards_list)

    db['Customers'] = rewardBR_dict
    db.close()

    return render_template('retrieveRewardBR1.html', count=len(rewards_list), customers_list=rewards_list)

@app.route('/updateRewardBR1/<int:id>/', methods=['GET', 'POST'])
def update_rewardBR1(id):
    if 'login' in session:
        if session['login'] == customer:
            update_rewardBR = UpdateRewardBR1(request.form)
            if request.method == 'POST' and update_rewardBR.validate():
                rewardBR_dict = {}
                db = shelve.open('customer.db', 'w')
                rewardBR_dict = db['Customers']
                userid = session['id']

                reward = rewardBR_dict.get(id)
                reward.set_first_name(update_rewardBR.first_name.data)
                reward.set_last_name(update_rewardBR.last_name.data)
                reward.set_gender(update_rewardBR.gender.data)
                reward.set_email(update_rewardBR.email.data)
                reward.set_date_joined(update_rewardBR.date_joined.data)
                reward.set_membership(update_rewardBR.membership.data)
                reward.set_status('Unavailable')
                reward.set_sessionid(userid)

                db['Customers'] = rewardBR_dict
                db.close()

                return redirect(url_for('home'))
            else:
                rewardBR_dict = {}
                db = shelve.open('customer.db', 'r')
                rewardBR_dict = db['Customers']
                db.close()

                reward = rewardBR_dict.get(id)
                update_rewardBR.first_name.data = reward.get_first_name()
                update_rewardBR.last_name.data = reward.get_last_name()
                update_rewardBR.gender.data = reward.get_gender()
                update_rewardBR.email.data = reward.get_email()
                update_rewardBR.date_joined.data = reward.get_date_joined()
                update_rewardBR.membership.data = reward.get_membership()

                return render_template('updateRewardBR1.html', form=update_rewardBR)

    else:
        return redirect(url_for('login'))

@app.route('/deleteRewardBR1/<int:id>', methods=['POST'])
def delete_rewardBR1(id):
    rewardBR_dict = {}
    db = shelve.open('customer.db', 'w')
    rewardBR_dict = db['Customers']

    rewardBR_dict.pop(id)

    db['Customers'] = rewardBR_dict
    db.close()

    return redirect(url_for('retrieve_rewardBR1'))

@app.route('/vrewardsBOX1')
def vrewardsBOX1():

    return render_template('vrewardsBOX1.html')

@app.route('/vboxes')
def vboxes():
    db = shelve.open('customer.db', 'w')
    rewardBR_dict = db['Customers']
    box = rewardBR_dict.get(1)
    status = box.get_status()
    box2 = rewardBR_dict.get(2)
    status2 = box2.get_status()
    box3 = rewardBR_dict.get(3)
    status3 = box3.get_status()

    return render_template('vboxes.html',status = status, status2 = status2, status3 = status3)

@app.route('/vboxes2')
def vboxes2():
    db = shelve.open('customer.db', 'w')
    rewardBR_dict = db['Customers']
    box = rewardBR_dict.get(4)
    status = box.get_status()
    box2 = rewardBR_dict.get(5)
    status2 = box2.get_status()
    box3 = rewardBR_dict.get(6)
    status3 = box3.get_status()

    return render_template('vboxes2.html',status = status, status2 = status2, status3 = status3)

@app.route('/vboxes3')
def vboxes3():
    db = shelve.open('customer.db', 'w')
    rewardBR_dict = db['Customers']
    box = rewardBR_dict.get(7)
    status = box.get_status()
    box2 = rewardBR_dict.get(8)
    status2 = box2.get_status()
    box3 = rewardBR_dict.get(9)
    status3 = box3.get_status()
    return render_template('vboxes3.html',status = status, status2 = status2, status3 = status3)

@app.route('/userbox')
def userbox():
    if 'login' in session:
        if session['login'] == customer:

            rewardBR_dict = {}
            db = shelve.open('customer.db', 'r')
            rewardBR_dict = db['Customers']
            db.close()
            sesID = session['id']
            onedaybefore = datetime.now().date() - timedelta(days=1)

            rewards_list = []
            for key in rewardBR_dict:
                reward = rewardBR_dict.get(key)
                check = reward.get_sessionid()
                if sesID == str(check):
                    if reward.get_date_joined() <= date.today():
                        reward.set_first_name('Enter your First Name')
                        reward.set_last_name('Enter your Last Name')
                        reward.set_gender('M')
                        reward.set_email('example@email.com')
                        reward.set_date_joined(date.today())
                        reward.set_membership('D')
                        reward.set_status('Available')
                        reward.set_sessionid('0')
                    else:
                        rewards_list.append(reward)

            RewardsBR.RewardsBR.count_id = len(rewards_list)

            return render_template('userbox.html', count=len(rewards_list), customers_list=rewards_list)

    else:
        return redirect(url_for('login'))

@app.route('/box_dashboard')
def box_dashboard():
    db = shelve.open('customer.db', 'r')
    customers = db['Customers']
    rented_boxes = [box for box in customers.values() if box.get_status() == 'Unavailable']
    count_per_day = [0] * calendar.monthrange(date.today().year, date.today().month)[1]

    for box in rented_boxes:
        rented_date = box.get_date_joined()
        if rented_date.month == date.today().month:
            count_per_day[rented_date.day-1] += 1

    boxdata = count_per_day
    return render_template('boxStat.html', boxdata=boxdata)

@app.route('/reward_dashboard')
def reward_dashboard():
    userID = session['id']
    count1 = 0
    db = shelve.open('test.db', 'r')
    check = db[userID]

    for key in check:
        count1 +=1


    boxdata = [count1]
    return render_template('rewardStat.html', boxdata=boxdata)

#if 'login' in session:
#    if session['login'] == customer/staff:
#
#    etc

    
#redeem reward is just like update/delete, make the button have an id [if frgt ask cher agn on wens]
#start with session
#play with session ID, link claimed reward to session ID (i.e joe claimed, joe's ID = 1; ID1 claimed coupon ID1)


#danzil's code vvv

from Forms import CreateLocationForm, CreateStoreForm, CreateListingForm
import Listing
from wtforms import FileField
import sys
DEBUG = sys.stdout.write

cart = []

#listings
@app.route('/createListing', methods=['GET', 'POST'])
def create_listing():
    create_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and create_listing_form.validate():
        listings_dict = {}
        db = shelve.open('listing.db', 'c')

        try:
            listings_dict = db['Listings']
        except:
            print("Error in retrieving Listings from listing.db.")

        listing = Listing.Listing(create_listing_form.listing_owner.data, create_listing_form.listing_name.data,
                         create_listing_form.listing_price.data, create_listing_form.listing_description.data,
                         create_listing_form.listing_stock.data, create_listing_form.listing_location.data)
        listings_dict[listing.get_listing_id()] = listing
        db['Listings'] = listings_dict

        db.close()

        return redirect(url_for('retrieve_listings'))
    return render_template('createListing.html', form=create_listing_form)

@app.route('/retrieveListings')
def retrieve_listings():
    listings_dict = {}
    db = shelve.open('listing.db', 'r')
    listings_dict = db['Listings']
    db.close()

    listings_list = []
    for key in listings_dict:
        listing = listings_dict.get(key)
        listings_list.append(listing)

    return render_template('retrieveListings.html', count=len(listings_list), listings_list=listings_list)

@app.route('/viewListings')
def view_listings():
    if 'login' in session:
        if session['login'] == customer:
            listings_dict = {}
            db = shelve.open('listing.db', 'r')
            listings_dict = db['Listings']
            db.close()

            listings_list = []
            for key in listings_dict:
                listing = listings_dict.get(key)
                listings_list.append(listing)

            return render_template('viewListings.html', count=len(listings_list), listings_list=listings_list)
        else:
            return redirect('/retrieveListings')

@app.route('/viewListings', methods=['GET', 'POST'])
def search_filter():
    listings_dict = {}
    db = shelve.open('listing.db', 'r')
    listings_dict = db['Listings']
    db.close()

    listings_list = []
    filterWord = request.form.get("search_term")
    for key in listings_dict:
        listing = listings_dict.get(key)
        if filterWord.lower() in listing.get_listing_location().lower():
            listings_list.append(listing)
    

    return render_template('viewListings.html', count=len(listings_list), listings_list=listings_list)

@app.route('/viewCart/<int:id>/', methods=['GET', 'POST'])
def add_to_cart(id):
    listings_dict = {}
    db = shelve.open('listing.db', 'w')
    listings_dict = db['Listings']
    
    listing = listings_dict.get(id) # replace this with your function that retrieves a specific listing from the database
    cart.append({
        "id": listing.get_listing_id(),
        "name": listing.get_listing_name(),
        "price": listing.get_listing_price()
    })

    DEBUG (str(cart))

    return redirect('/viewCart')

@app.route('/viewCart/<int:id>/delete', methods=['GET', 'POST'])
def remove_from_cart(id):
    listings_dict = {}
    db = shelve.open('listing.db', 'w')
    listings_dict = db['Listings']
    listing = listings_dict.get(id)
    cart.pop(id)

    DEBUG (str(cart))

    return render_template("cart.html", cart=cart)

@app.route('/updateListing/<int:id>/', methods=['GET', 'POST'])
def update_listing(id):
    update_listing_form = CreateListingForm(request.form)
    if request.method == 'POST' and update_listing_form.validate():
        listings_dict = {}
        db = shelve.open('listing.db', 'w')
        listings_dict = db['Listings']

        listing = listings_dict.get(id)
        listing.set_listing_owner(update_listing_form.listing_owner.data)
        listing.set_listing_name(update_listing_form.listing_name.data)
        listing.set_listing_price(update_listing_form.listing_price.data)
        listing.set_listing_description(update_listing_form.listing_description.data)
        listing.set_listing_stock(update_listing_form.listing_stock.data)
        listing.set_listing_location(update_listing_form.listing_location.data)

        db['Listings'] = listings_dict
        db.close()

        return redirect(url_for('retrieve_listings'))
    else:
        listings_dict = {}
        db = shelve.open('listing.db', 'r')
        listings_dict = db['Listings']
        db.close()

        listing = listings_dict.get(id)
        update_listing_form.listing_owner.data = listing.get_listing_owner()
        update_listing_form.listing_name.data = listing.get_listing_name()
        update_listing_form.listing_price.data = listing.get_listing_price()
        update_listing_form.listing_description.data = listing.get_listing_description()
        update_listing_form.listing_stock.data = listing.get_listing_stock()
        update_listing_form.listing_location.data = listing.get_listing_location()
        return render_template('updateListing.html', form=update_listing_form)

@app.route('/deleteListing/<int:id>', methods=['POST'])
def delete_listing(id):
    listings_dict = {}
    db = shelve.open('listing.db', 'w')
    listings_dict = db['Listings']
    listings_dict.pop(id)

    db['Listings'] = listings_dict
    db.close()

    return redirect(url_for('retrieve_listings'))
 
@app.route('/viewCart', methods=["GET", "POST"])
def viewCart():
    
    return render_template("cart.html", cart=cart)

#end of Danzil's code

if __name__ == '__main__':
    app.run(debug=True)
