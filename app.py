from random import randint
from time import strftime
from flask import Flask, Markup, flash, render_template, request
from pywallet import wallet
from wtforms import DateField, Form, StringField, SubmitField, TextField, TextAreaField, validators

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = b'P\x0f\xdb4v\xdc\x15\n\xc9s\x9a\xbb\x95\xfb\xe9\xdc'

 # username = StringField('Username', [validators.Length(min=4, max=25)])
 #    email = StringField('Email Address', [validators.Length(min=6, max=35)])
 #    password = PasswordField('New Password', [
 #        validators.DataRequired(),
 #        validators.EqualTo('confirm', message='Passwords must match')
 #    ])
 #    confirm = PasswordField('Repeat Password')
 #    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class ReusableForm(Form):
    #frn = TextField('FRN:', validators  = [validators.required()])
    frn = StringField('FRN', [validators.Length(min = 10, max = 10)])
    frn_expiry = DateField('FRN_Expiry', validators = [validators.required()])
    domain = StringField('Domain', [validators.Length(min = 6, max = 9)])
    facility_id = TextField('Facility_ID', validators  = [validators.required()])

def get_time():
    time = strftime("%Y-%m-%dT%H:%M")
    return time

def write_to_disk(frn, frn_expiry, domain, facility_id):
    data = open('file.log', 'a')
    timestamp = get_time()
    data.write('DateStamp = {}, FRN = {}, FRN_Expiry = {}, Domain = {}, Facility_ID = {} \n'.format(timestamp, frn, frn_expiry, domain, facility_id))
    data.close()

@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        frn = request.form['frn']
        frn_expiry = request.form['frn_expiry']
        domain = request.form['domain']
        facility_id = request.form['facility_id']

        if form.validate():
            write_to_disk(frn, frn_expiry, domain, facility_id)
            flash('Valid FRN: {} Valid till: {}'.format(frn, frn_expiry))
            flash('Verified SSL Certificate: {} Valid till: {}'.format(domain, facility_id))
            seed = wallet.generate_mnemonic()
            w = wallet.create_wallet(network = "ETH", seed = seed, children = 1)
            ethereum_address = w.get('address')
            seed_phrase = w.get('seed')
            flash(Markup('Ethereum address created successfully: <br> <b> {} </b>'.format(ethereum_address)))
            flash(Markup('Store the corresponding Seed Phrase safely and import it into your Metamask Browser Extension: <br> <b> {} </b>'.format(seed_phrase)))
            flash(Markup('Successfully registered, please click <a href="https://faucet.rinkeby.io/" class="alert-link">here to send your new address some test ether on Rinkeby</a>'))
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash('Error: {} {}'.format(fieldName, err))
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run()
    '''
        # Connect to local node
        try:
            api = ipfsapi.connect('127.0.0.1', 5001)

            #new_file = api.add('new.txt')
            res = api.cat('QmWvgsuZkaWxN1iC7GDciEGsAqphmDyCsk3CVHh7XVUUHq')
            print(res)

        except ipfsapi.exceptions.ConnectionError as ce:
            print(str(ce))
'''
