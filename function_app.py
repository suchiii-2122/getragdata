import azure.functions as func
import logging, os, json


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="gitpushpublish")
def gitpushpublish(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    from azure.search.documents import SearchClient
    from azure.core.credentials import AzureKeyCredential
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    try:
        endpoint = os.getenv("SEARCH_ENDPOINT")
        index_name = os.getenv("SEARCH_INDEX_NAME")
        key = os.getenv("SEARCH_ADMIN_KEY")
        if not all([endpoint,index_name,key]):
            # raise ValueError
            return func.HttpResponse(
             " Failed to get all key points",
             status_code=500
        )
    except Exception as e:
        logging.error(f'failed to get the endpoints')
    try:
        search_client = SearchClient(
        endpoint=os.getenv("SEARCH_ENDPOINT"), # type: ignore
        index_name=os.getenv("SEARCH_INDEX_NAME"), # type: ignore
        credential=AzureKeyCredential(os.getenv("SEARCH_ADMIN_KEY")) # type: ignore
    )
        return func.HttpResponse(
            json.dumps("successfully intialized the search client"),
            status_code=200
        )
    except Exception as e:
        logging.error(f'Failed to create search client: {e}')
        return func.HttpResponse(
             json.dumps(f'Failed to create search client: {e}'),
             status_code=500
        )


    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully, now . Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )