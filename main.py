
from flask import Flask, jsonify
from flask import request
from flask.views import MethodView
from models import User, Session, Ad

app = Flask(__name__)



class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.close()
    return response

def get_user_by_id(id: int):
    user = request.session.get(User, id)
    if user is None:
        raise HttpError(404, "user not found")
    return user 

def get_ad_by_id(id: int):
    ad = request.session.get(Ad, id)
    if ad is None:
        raise HttpError(404, "ad not found")
    return ad
    

class UserView(MethodView):
    def get(self, id:int):
        user = get_user_by_id(id)
        return jsonify({'id': user.id, 'name': user.name, 'registration_time': user.registration_time.isoformat()})
    
    def post(self):
        json_data = request.json
        user = User(**json_data)
        request.session.add(user)
        request.session.commit()
        return jsonify({'id': user.id})
    
    def patch(self, id:int):
        user = get_user_by_id(id)
        return jsonify({'http_method': 'PATCH', 'hello': 'world'})
    
    def delete(self, id:int):
        user = get_user_by_id(id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({'deleted': user.id})
    

class AdView(MethodView):
    def get(self, id: int):
        ad = get_ad_by_id(id)
        return jsonify({'id': ad.id,
                        'title': ad.title,
                        'description': ad.description,
                        'time': ad.registration_time,
                        'owner': ad.owner_id})

    def post(self):
        json_data = request.json
        ad = Ad(**json_data)
        request.session.add(ad)
        request.session.commit()
        return jsonify({'id': ad.id,
                        'title': ad.title,
                        'description': ad.description,
                        'time': ad.registration_time,
                        'owner': ad.owner_id})

    def delete(self, id: int):
        ad = get_ad_by_id(id)
        request.session.delete(ad)
        request.session.commit()
        return jsonify({'ad_view': 'DELETE'})


user_view = UserView.as_view('user_view')
ad_view = AdView.as_view('ad_view')
app.add_url_rule('/user/', view_func=user_view, methods=['POST'])
app.add_url_rule('/user/<int:id>/', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ad/', view_func=ad_view, methods=['POST'])
app.add_url_rule('/ad/<int:id>/', view_func=ad_view, methods=['GET', 'DELETE'])


app.run()