from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import dataset,sendgrid
app = Flask(__name__)
# Connect to sendgrid
sg = sendgrid.SendGridClient('','')
# Connnect to database
db = dataset.connect('sqlite:///names.db')
# create your guests table
table = db['guests']
# when someone sends a GET to / render sign_form.html
@app.route('/', methods=['GET'])
def sign_form():
    return render_template('sign_form.html')

# when someone sends a GET to /guest_book render guest_book.html
@app.route('/guest_book', methods=['GET'])
def guest_book():
    signatures = table.find()
    return render_template('guest_book.html', signatures=signatures)

# when someone sends  POST to /submit, take the name and message from the body
# of the POST, store it in the database, and redirect them to the guest_book
@app.route('/submit', methods=['POST'])
def submit():
    signature = dict(name=request.form['name'], message=request.form['message'])
    table.insert(signature)
    return redirect(url_for('guest_book'))

# if someone then wants to share the basil with someone else, they can do it here.  
@app.route('/email',methods=['POST'])
def process():
	email = request.form['email']	
	print str(email)
	###sendgrid sends an email to friends.  
	message=sendgrid.Mail()
	message.add_to(str(email)) 
	message.add_bcc('davidawad64@gmail.com') ##sends me a BCC of the email for debugging ##
	message.set_subject("Basil is Love, Basil is Life") ##reassures the customer
	message.set_html('try.html')
	message.set_text('Your Friends think you should come up with a Nicknmame for basil! You should try it! Go to Basildb.me today! Sincerely, The Basil Ahmad Foundation.')
	message.set_from('The Basil Ahmad Foundation <Admin@basildb.me>')
	#status, msg = sg.send(message)
	return

@app.errorhandler(404)
def new_page(error):
	return render_template("404.html") 

app.run(debug=True)
