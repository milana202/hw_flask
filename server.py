from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advertisement
from schema import CreateAdv, PatchAdv, VALIDATION_CLASS
from pydantic import ValidationError

# создаю экземпляр класса
app = Flask("app")

class HttpError(Exception):

    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {
        'status': 'error',
        'decription': error.message
    }
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response

def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict()
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict

def get_adv(session: Sesson, adv_id: int):
    adv = session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, "The advertisement doesn't exist")
    return adv


class AdvertisementView(MethodView):

    def post(self):
        json_data = validate_json(request.json, CreateAdv)
        with Sesson() as session:
            adv = Advertisement(**json_data)
            session.add(adv)
            session.commit()
            return jsonify({'id':adv.id})

    def get(self, adv_id: int):
        with Sesson() as session:
            adv = get_adv(session, adv_id)
            return jsonify({'id': adv.id,
                            'description': adv.description,
                            'created dete': adv.created_date.isoformat(),
                            'owner': adv.owner})

    def putch(self, adv_id: int):
        json_data = validate_json(request.json, PatchAdv)
        with Sesson() as session:
            adv = get_adv(session, adv_id)
            for field, value in json_data.items():
                setattr(adv, field, value)
            session.add(adv)
            session.commit
            return jsonify({'id': adv.id,
                            'description': adv.description,
                            'created dete': adv.created_date.isoformat(),
                            'owner': adv.owner})

    def delete(self, adv_id: int):
        with Sesson() as session:
            adv = get_adv(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({'status': 'successful'})


app.add_url_rule(
    '/adv/<int:adv_id',
    view_func=AdvertisementView.as_view('with_adv_id'),
    methods=['GET', 'PUTCH', 'DELETE']
)
app.add_url_rule(
    '/adv/',
    view_func=AdvertisementView.as_view('create_advertisement'),
    methods=['POST']
)


if __name__ == '__main__':
    app.run()