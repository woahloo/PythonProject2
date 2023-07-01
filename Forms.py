from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, FileField, FloatField, IntegerField
from wtforms.fields import EmailField, DateField
from datetime import date, timedelta
from wtforms.validators import ValidationError
import re


def date_is_future(form, field):
    if field.data < date.today():
        raise ValidationError("The date must be a date after today.")

def validate_email(form, field):
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, field.data):
        raise ValidationError("Invalid email format")

class CreateUserForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = RadioField('Have you bought from us before?', choices=[('Y', 'Yes'), ('N', 'No')], default='N')
    remarks = TextAreaField('Location', [validators.Optional()])

class CreateCustomerForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField("Email", [validators.DataRequired(), validate_email])
    date_joined = DateField('Date until', format='%Y-%m-%d', validators=[date_is_future])
    address = RadioField('Box Number', choices=[('1', '1'), ('2', '2'), ('3', '3')], default='F')
    membership = RadioField('Existing Box Owner', choices=[('D', 'Yes'), ('W', 'No')], default='F')
    remarks = TextAreaField('Location', [validators.Optional()])

class UpdateRewardBR1(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = StringField("Email", [validators.DataRequired(), validate_email])
    date_joined = DateField('Date until', format='%Y-%m-%d', validators=[date_is_future])
    membership = RadioField('Existing Box Owner', choices=[('D', 'Yes'), ('W', 'No')], default='F')

#danzil part

class CreateLocationForm(Form):
    location_name = StringField('Location Name', [validators.Length(min=1, max=150, message="Name cannot be longer than 150 Characters."), validators.DataRequired(message="Field is Required!")])
    location_image = StringField('Location Name', [validators.Length(min=1, max=150, message="Name cannot be longer than 150 Characters."), validators.DataRequired(message="Field is Required!")])

class CreateStoreForm(Form):
    store_name = StringField('Store Name', [validators.Length(min=1, max=150, message="Name cannot be longer than 150 Characters"), validators.DataRequired(message="Field is Required!")])
    store_category = SelectField('Store Category', choices=[('A', 'Accessories'), ('C', 'Clothes'), ('T', 'Toys'), ('O', 'Others'), ('S', 'Stickers'), ('K', 'Kids'), ('G', 'Gadgets')], default='O')

class CreateListingForm(Form):
    listing_owner = StringField('Listing Owner', [validators.Length(min=1, max=150, message="Name cannot be longer that 150 Characters"), validators.DataRequired(message="Field is Required!")])
    listing_name = StringField('Listing Name', [validators.Length(min=1, max=150, message="Name cannot be longer than 150 Characters."), validators.DataRequired(message="Field is Required!")])
    listing_price = FloatField('Listing Price', [validators.NumberRange(min=0,max=9999999, message="Please enter a valid value."), validators.DataRequired(message="Please enter a valid number!"),])
    listing_description = StringField('Listing Description', [validators.Length(min=1, max=800, message="Description cannot be longer that 800 Characters."), validators.DataRequired(message="Field is Required!")])
    listing_stock = IntegerField('Listing Stock', [validators.NumberRange(min=0,max=9999, message="Please enter a valid amount"), validators.DataRequired(message="Field is Required!")])
    listing_location = StringField('Location Name', [validators.Length(min=1, max=150, message="Name cannot be longer than 150 Characters."), validators.DataRequired(message="Field is Required!")])

#end of danzil part