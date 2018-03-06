import json
from botocore.vendored import requests

search_url_1 = "/ws/v11/gh/search"
search_url_2 = "?$lang=en-US&portalId="
common_url_3 = "&usertype=customer"
article_url_1 = "/ws/v11/ss/article/"
article_url_2 = '?$attribute=name,id,content,availableEditions&$lang=en-US&context=article_view_guided_help&portalId='

headers = {
    'cache-control': 'no-cache',
    'Accept': 'application/json'
}

def invokeCaseBase(base_url, portal, casebase, ivr_stage, stored_data):
    sub_resource = '/start'
    print("Amazon Connect Stored Data from previous eGain Call ")
    print(stored_data)
    data = {'casebaseId': casebase}
    if ivr_stage != 'MAIN':
        sub_resource = ""
    if len(stored_data) > 0 and stored_data != 'null':
        stored_data = json.loads(stored_data)
        headers['X-egain-session'] = stored_data['X-egain-session']
        try:
            if 'Q1' in stored_data['qn']:
                data[stored_data['qn']] = stored_data['ans' + str(ivr_stage)]
            elif 'Q' in stored_data['qn']:
                data[stored_data['qn']] = str(ivr_stage)

        except KeyError:
            print('failed to get qn and answers in stored data')

    url = base_url + search_url_1 + sub_resource + search_url_2 + portal + common_url_3
    print("Casebase request Details")
    print(url)
    print(headers)
    print(data)
    response = requests.post(url, data=data, headers=headers)
    return_val = {}
    json_data = {}
    try:
        output = response.json()
        print("Casebase Response Object")
        print(output)
        return_val['X-egain-session'] = response.headers['X-egain-session']
        if output["callInfo"]['status'] == 'success':
            if len(output['unansweredQuestion']) > 0:
                json_data['script'] = output['unansweredQuestion'][0]['title']
                return_val['qn'] = 'Q' + output['unansweredQuestion'][0]['type'] + '-' + str(
                    output['unansweredQuestion'][0]['format']) + '-' + str(
                    output['unansweredQuestion'][0]['id'])
                ans_count = 1
                for ans in output['unansweredQuestion'][0]['validAnswer']:
                    return_val['ans' + str(ans_count)] = ans['id']
                    ans_count += 1
            elif len(output["actionSearch"]) > 0:
                if output["actionSearch"][0]['score'] == 100:
                    article_id = output["actionSearch"][0]['alternateId']
                    article_url = base_url + article_url_1 + article_id + article_url_2 + portal + common_url_3
                    print("article details fetching request")
                    print(article_url)
                    article_response = requests.get(article_url, params=None, headers=headers)
                    article_response_json = article_response.json()
                    print("article details fetched from server")
                    print(article_response_json)
                    json_data["queue"] = article_response_json["article"][0]['customAttribute'][0]['value']
                    json_data['script'] = article_response_json["article"][0]['name']
                    json_data['ivrended'] = 'true'
                    count = 1
                    for x in output['answeredQuestion']:
                        json_data["ans" + str(count)] = x['previousAnswer'][0]['text']
                        count += 1


    except:
        print("Error occured")
        print(response.text)
        raise Exception(response.text)
    if len(return_val) > 0:
        json_data["storedData"] = json.dumps(return_val)

    print("response sent to Connect Instance")
    print(json_data)
    return json_data