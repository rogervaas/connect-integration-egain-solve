import os, json
from invokecb import invokeCaseBase

search_url_1 = "/ws/v11/gh/search"
search_url_2 = "?$lang=en-US&portalId="
common_url_3 = "&usertype=customer"
article_url_1 = "/ws/v11/ss/article/"
article_url_2 = '?$attribute=name,id,content,availableEditions&$lang=en-US&context=article_view_guided_help&portalId='

headers = {
    'cache-control': 'no-cache',
    'Accept': 'application/json'
}

def lambda_handler(event, context):
    print("Amazon Connect Event ")
    print(event)
    base_url = getOsEnv("BASE_URL")
    portal = getOsEnv("PORTAL_ID")
    casebase = getOsEnv("CASEBASE_ID")
    stored_data = 'null'
    event_data = json.loads(event)
    if 'storedData' in event_data:
        stored_data = event['Details']['ContactData']['Attributes']['storedData']
    ivr_stage = 'MAIN'
    if 'IVRStage' in event_data:
        ivr_stage = event['Details']['ContactData']['Attributes']['IVRStage']

    json_data = {}
    json_data = invokeCaseBase(base_url, portal, casebase, ivr_stage, stored_data)
    return json_data


def getOsEnv(name):
  if name not in os.environ:
    msg = name +" enviroment variable is missing"
    print(msg)
    raise Exception(msg)
  return os.environ[name]
