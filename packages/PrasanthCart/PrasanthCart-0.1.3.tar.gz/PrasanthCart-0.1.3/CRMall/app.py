from flask import Flask, request
from flask_restful import reqparse, Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
app = Flask(__name__)
api = Api(app)
CORS(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#-------------------------------------------Roles---------------------------------------------------------------------------

from controllers.roles.post_roles import Getcreateroles
from controllers.roles.roles import GetUpdateDeleteRoles
api.add_resource(Getcreateroles, '/addrole')
api.add_resource(GetUpdateDeleteRoles, '/getupdatedeleteroles/<int:id>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
