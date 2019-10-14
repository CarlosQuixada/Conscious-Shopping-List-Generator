# from Util import Util
import json

from flask import Flask, request, jsonify

from app.genetic_algorithm import GeneticAlgorithm

# from flask_cors import CORS, cross_origin
# from gevent.pywsgi import WSGIServer
# from healthcheck import HealthCheck, EnvironmentDump
# from flasgger import Swagger, swag_from

api = Flask('CSLG')

# Documentation
'''
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Delfos Documentation",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.1.1",
            "title": "Delfos V1",
            "endpoint": 'v1_spec',
            "description": 'Essa é a versão 1 do Delfos',
            "route": '/v1/spec'
        }
    ]
}

swagger = Swagger(app)
'''


@api.route('/')
def heath_check():
    """
    Método utilizado como health check
    :return: retorna apenas um 200 para confirmar que a API está de pé
    """
    return "Faaaaaalllaaaa Galera blz?", 200


@api.route('/generate-list', methods=['POST'])
# @swag_from('documentation/complain_diderot_classification.yml')
def generate_list():
    try:
        dreams_string = json.dumps(request.json, ensure_ascii=False)
        dreams = json.loads(dreams_string)

        genetic_algorithm = GeneticAlgorithm(dreams['limit'], dreams['dreams'])
        response = genetic_algorithm.generate_list()

        return response

    except Exception as e:
        return jsonify({"Exception": str(e)})


@api.errorhandler(404)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 404 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 404


@api.errorhandler(500)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 500 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 500


@api.errorhandler(400)
def page_not_found(e):
    """
        Método responsável pelo tratamento do erro 400 de acesso
    :param e: Exceção ocorrida
    :return: predição vazia
    """
    pred = {"predictions": [None, None, None], "complain": None, "Exception": e}
    return json.dumps(pred), 400


if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=False)
