import boto3
import json

client = boto3.client('elbv2')

loadbalancers = client.describe_load_balancers()

new_list = []
json_obj = ""

for loadbalancer in loadbalancers['LoadBalancers']:
    lb = dict(loadbalancer)
    lb['CreatedTime'] = ""
    lb['Listeners'] = [] 
    listeners = client.describe_listeners(LoadBalancerArn=loadbalancer['LoadBalancerArn'])
    for listener in listeners['Listeners']:
        lb['Listeners'].append(listener)
    new_list.append(lb)
    json_obj = json.dumps(new_list, indent = 2 )
print(json_obj)
