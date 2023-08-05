from models import Roles
from config import ma,db
from marshmallow.fields import Nested

class RolesSchema(ma.ModelSchema):
    class Meta:
        model =Roles
        fields = ('id','name','status','created_at','updated_at')
        sqla_session = db.session

class RolesGetSchema(ma.ModelSchema):
    class Meta:
        model = Roles
        sqla_session = db.session
