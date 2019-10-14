# CSLG API

This application generates dream list-based shopping suggestion lists and how much you can spend on that purchase.

## Technology
![Alt text](images/python+flask.jpg?raw=true "Python and Flask")
github Flask: https://github.com/pallets/flask

![Alt text](images/deap.png?raw=true "DEAP")
github DEAP: https://github.com/DEAP/deap

## Workspace
* `$ git clone git@github.com:CarlosQuixada/Conscious-Shopping-List-Generator.git`
* `$ cd Conscious-Shopping-List-Generator`
* `$ pip install -r requirements.txt`

## Execution
* `$ python run.py`
* Visit the app at http://localhost:5000/

### Use

To generate purchase suggestion list you must send a POST to endpoint / generate-list
with the following format:

```
{
    "limit": 100.10,
    "dreams": [
        {
            "name": "product name",
            "price": 50.00
        },
        {
            "name": "product name",
            "price": 60.50
        },
        {
            "name": "product name",
            "price": 10.00
        }
    ]
}
```

*Built by Carlos Quixadá*
