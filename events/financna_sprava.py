
import requests
from requests.structures import CaseInsensitiveDict

url = "https://ekasa.financnasprava.sk/mdu/api/v1/opd/receipt/find"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"


def check_recipt(uid):

	data = '{"receiptId":"' + str(uid) + '"}'

	resp = requests.post(url, headers=headers, data=data)

	print(resp, uid)

	data_r = resp.json()

	return data_r
