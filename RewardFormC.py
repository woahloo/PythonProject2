from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, ValidationError
from wtforms.fields import EmailField, DateField, PasswordField
from datetime import date

class CreateRewardBR(Form):
    def dateIssueC(form, field):
        if field.data == None:
            raise ValidationError("Please select a date!")
        if field.data < date.today():
            raise ValidationError("The date must be a date today, or after today.")

    def dateExpiryC(form, field):
        if field.data == None:
            raise ValidationError("Please select a date!")
        if field.data < date.today():
            raise ValidationError("The date must be a date today, or after today.")
        if field.data < form.issueDate.data:
            raise ValidationError("The date cannot be before the issue date!")

    #Form
    coupon_name = StringField('Coupon Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    rType = SelectField('Reward Type', [validators.DataRequired()], choices=[('', 'Select'), ('gift', 'Gift'), ('discount', 'Discount')], default='')
    issueDate = DateField('Issue Date', format='%Y-%m-%d', validators=[dateIssueC])
    expiryDate = DateField('Expiry Date', format='%Y-%m-%d', validators=[dateExpiryC])
    code = StringField('Coupon Code (Start with the first 2 letters of coupon name)', [validators.Length(min=8, max=8), validators.Regexp(r'^[A-Za-z]{2}\d{6}$')])
    description = TextAreaField('Description', [validators.DataRequired()])

class CreateRewardBOX(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    #email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('F', 'Fellow'), ('S', 'Senior'), ('P', 'Professional')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])

class UpdateRewardBR(Form):
    def dateExpiryC(form, field):
        if field.data == None:
            raise ValidationError("Please select a date!")
        if field.data < date.today():
            raise ValidationError("The date must be a date today, or after today.")
        if field.data < form.issueDate.data:
            raise ValidationError("The date cannot be before the issue date!")

    #Form
    status = SelectField('Status', [validators.DataRequired()], choices=[('Active', 'Active'), ('Expired', 'Expired')], default='active')
    coupon_name = StringField('Coupon Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    rType = SelectField('Reward Type', [validators.DataRequired()], choices=[('', 'Select'), ('gift', 'Gift'), ('discount', 'Discount')], default='')
    issueDate = DateField('Issue Date', format='%Y-%m-%d')
    expiryDate = DateField('Expiry Date', format='%Y-%m-%d', validators=[dateExpiryC])
    code = StringField('Coupon Code', [validators.Length(min=8, max=8), validators.Regexp(r'^[A-Za-z]{2}\d{6}$')])
    description = TextAreaField('Description', [validators.DataRequired()])

class LoginForm(Form):
    user_name = StringField('User Name', [validators.Length(min=1, max=999)])
    password = PasswordField('Password', [validators.Length(min=1, max=999)])
