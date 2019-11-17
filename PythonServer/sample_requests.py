import requests


hostname = 'http://127.0.0.1:8000'


# print(requests.get('{}/pills/1'.format(hostname)).json())
#
#
# new_pill = {
#     "patient_id": 1,
#     "name": "HIIIII",
#     "quantity": 18,
#     "time": "14:00:00",
#     "dose": 2
# }
# print(requests.post('{}/new/pill'.format(hostname), json=new_pill).json())
#
#
# updated_pill = {
#     "patient_id": 1,
#     "name": "HIIIII",
#     "quantity": 10,
#     "time": "14:00:00",
#     "dose": 2
# }
# print(requests.put('{}/pill/15'.format(hostname), json=updated_pill))


print(requests.post('{}/dispense'.format(hostname), json={"id": 2}))


# print(requests.post('{}/remind'.format(hostname), json={"id": 1}))
