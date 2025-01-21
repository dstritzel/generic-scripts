import boto3

client = boto3.client('elbv2')

loadbalancers = client.describe_load_balancers(names=['my-loadbalancer'])

new_list = []

for loadbalancer in loadbalancers['LoadBalancers']:
    lb = loadbalancer;
    lb['Listeners'] = [] 
    listeners = client.describe_listeners(LoadBalancerArn=loadbalancer['LoadBalancerArn'])
    for listener in listMoeners['Listeners']:
        lb['Listeners'].append(listener)
        lb['Listeners']['Rules'] = []
        rules = client.describe_rules(ListenerArn=listener['ListenerArn'])
        for rule in rules['Rules']:
            lb['Listeners']['Rules'].append(rule)
    print(new_list)