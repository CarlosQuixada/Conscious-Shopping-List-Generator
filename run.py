# from Util import Util
import json

from flask import Flask, request, jsonify

from app.genetic_algorithm import GeneticAlgorithm

# from flask_cors import CORS, cross_origin
# from gevent.pywsgi import WSGIServer
# from healthcheck import HealthCheck, EnvironmentDump
# from flasgger import Swagger, swag_from

api = Flask('CSLG')

# COR configurations
# CORS(app, resources={r"/classify": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

# Neura Network Loading
# util = Util()

# healthcheck
# health = HealthCheck()
# envdump = EnvironmentDump()


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
'''
@app.after_request
def after_request(response):
    """
        Método responsável pela tratamento de CORS da aplicação
    :param response: reposta de cada requisição na API
    :return: retorno da API com o cabeçalho de tratamento de CORS
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
'''


@api.route('/')
# @cross_origin()
def heath_check():
    """
    Método utilizado como health check
    :return: retorna apenas um 200 para confirmar que a API está de pé
    """
    return "Faaaaaalllaaaa Galera blz?", 200


# def classfy_by_part(name):

# health.add_check(heath_check)


'''
def application_data():
    return {"maintainer": "Diego Santos",
            "git_repo": "https://gitlab.com/trustvox/ai/delfos"}


envdump.add_section("application", application_data)
# Add a flask route to expose information
app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())
'''


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
        return jsonify({"Exception": e})


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
