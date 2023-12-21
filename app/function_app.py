import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="HttpExample")
@app.route(route="hello")
def hello_get(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("HttpExample function processed a request!")