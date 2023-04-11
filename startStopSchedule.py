import boto3,json


def checkKey(dict,key):
    tv=""
    for t in keyvalues:
        tv=t[valuename] if t['key'] == keyname  else tv
    return tv

def lambda_handler(event,context):
    t_Sch='StartStop-Schedule'
    t_Maint='Maintenance-StartStop-Schedule'
    filterTag,filterName={},[]
    if checkKey(event,'Tags'):
        for tag in event["Tags"]:
            filterTag[tag]=event["Tags"][tag].lower()
    if checkKey(event,'InstanceNames'):
        filterName=[x.lower() for x in (event['InstanceNames'].split(","))] if event['InstanceName'] != "*" else filterName
    p_Ids,p_CIds,p_before,p_after=[],[],[],[]
    ec2=boto3.client('ec2')
    el=ec2.describe_instances()
    for reservation in el['Reservations']:
        for instance in reservation['Instances']:
            p_Valid=True
            if checkKey(instance,'Tags'):
                for key in filterTag:
                    p_Valid=False if getKeyValue(isinstance['Tags'],key,'Value').lower() != filterTag[key] else p_Valid
            if filterName:
                p_Valid=False if getKeyValue(instance['Tags'],"Name","Value").lower() not in filterName else p_Valid
            if p_Valid:
                p_Ids.append(instance['InstanceId'])
    result={"RequestType": event["RequestType"] }
    if (p_Ids):
        el= ec2.describe_instances(InstanceIds=p_Ids)
        for reservation in el['Reservations']:
            for instnace