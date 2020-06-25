from cloudant.client import Cloudant

# Create client using auto_renew to automatically renew expired cookie auth
client = Cloudant('admin', 'password', url='http://192.168.2.211:5984',
                 connect=True,
                 auto_renew=True)


my_database = client['animes_td']

selector = {'recomendado': {'$gt': 0}}
docs = my_database.get_query_result(selector)
for doc in docs:
    print(doc)

r = my_database.get_view_result('_design/view1', 'new-view')

for r1 in r:
    print(r1['value']['titulo'])