import cfnresponse
import traceback
from invokecb import invokeCaseBase


def handler(event, context):
    try:
        if event['RequestType'] == 'Create':
            # Test Integration
            print('test eGain AI Integration')
            base_url = event['ResourceProperties']['BASE_URL']
            portal = event['ResourceProperties']['PORTAL_ID']
            casebase = event['ResourceProperties']['CASEBASE_ID']
            stored_data = 'null'
            ivr_stage = 'MAIN'

            json_data = {}
            json_data = invokeCaseBase(base_url, portal, casebase, ivr_stage, stored_data)
            print("response data: ")
            print(json_data)
            if "storedData" not in json_data or \
                    'X-egain-session' not in json_data["storedData"]:
                raise Exception('Error: failed to get successful response')
        elif event['RequestType'] == 'Update':
            pass
        elif event['RequestType'] == 'Delete':
            pass
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, '')
    except:
        print(traceback.print_exc())
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, '')
