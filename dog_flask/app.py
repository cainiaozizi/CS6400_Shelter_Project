from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import datetime


from security import authenticate, identity
from applicant import Applicant, ApplicantList
from adoptionapplication import AddApplication, LastApplication
from volunteer import Volunteer
from applicationReview import ApplicationReview, OneApplication, applicationapprove, applicationreject
from addadoption import EligibleApplication, LatestApplication,SelectedDogFee,SubmitAdoption
from RoleCheck import Admin
#
from dog_dashboard import dog_dashboard, dogindex
from add_dog import add_dog
from allbreeds import allbreeds
from edit_dog import edit_dog
from expense import expense
from reports import animal_control_report, animal_control_detail_1, animal_control_detail_2, adoption_report, expense_report



app = Flask(__name__)
app.secret_key = 'testsecret'
api = Api(app)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

jwt = JWT(app, authenticate, identity)
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(minutes=45)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin',
                         'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,Set-Cookie,Cookie,Cache-Control,Pragma,Expires')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE')
    return response

# AddAdoption Application
api.add_resource(ApplicantList, '/api/applicant')
api.add_resource(Applicant, '/api/applicant/<string:email_address>')
api.add_resource(AddApplication, '/api/applicant/<string:email_address>/addapplication')
api.add_resource(LastApplication, '/api/applicant/<string:email_address>/addapplication/success')


# ApplicationReview
api.add_resource(ApplicationReview, '/api/applicationreview')
api.add_resource(OneApplication, '/api/applicationreview/<string:ApplicationID>')
api.add_resource(applicationreject, '/api/applicationreject/<string:ApplicationID>')
api.add_resource(applicationapprove, '/api/applicationapprove/<string:ApplicationID>')

# AddAdoption
api.add_resource(EligibleApplication, '/api/eligibleapplication/<string:last_name>')
api.add_resource(LatestApplication, '/api/latestapplication/<string:Applicant_email>')
api.add_resource(SelectedDogFee, '/api/eligibleapplicationcoap/<string:dog_ID>')
api.add_resource(SubmitAdoption, '/api/submitadoption')

# Volunteer Review
api.add_resource(Volunteer, '/api/volunteer/<string:searchname>')

# Dog
api.add_resource(dog_dashboard, '/api/dog_dashboard', endpoint = 'dog_dashboard')
api.add_resource(dogindex, '/api/dogindex/<string:dog_ID>', endpoint = 'dogindex')
api.add_resource(add_dog, '/api/add_dog', endpoint = 'add_dog')
api.add_resource(allbreeds, '/api/allbreeds', endpoint = 'allbreeds')
api.add_resource(edit_dog, '/api/edit_dog/<string:dog_ID>', endpoint = 'edit_dog')

# Expense
api.add_resource(expense, '/api/expense/<string:dog_ID>', endpoint = 'expense')

# Reports
api.add_resource(animal_control_report, '/api/reports/animal_control_report', endpoint = 'animal_control_report')
api.add_resource(animal_control_detail_1, '/api/reports/animal_control_detail_1/<string:year_month>', endpoint = 'animal_control_detail_1')
api.add_resource(animal_control_detail_2, '/api/reports/animal_control_detail_2/<string:year_month>', endpoint = 'animal_control_detail_2')
api.add_resource(adoption_report, '/api/reports/adoption_report', endpoint = 'adoption_report')
api.add_resource(expense_report, '/api/reports/expense_report', endpoint = 'expense_report')

# Return if Admin
api.add_resource(Admin, '/api/Admin')

if __name__ =='__main__':
    app.run(debug=True)