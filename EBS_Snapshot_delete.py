import boto3
def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    #get all EBS snapshot
    response = ec2.describe_snapshots(OwnerIds=['self'])


    #get all active EC2 instance IDS
    instances_response = ec2.describe_instances(Filters=[{'Name' : 'instance-state-name', 'Values' : ['running']}])
    active_instance_ids =  set()

    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])
    
    #Iterate through each snapshot and delete if it is not attached to any volume

    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeID')

        if not volume_id:
            #delete the snapshot if it is not attached to any volume
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f"Deleted EBS snapshot {snapshot_id} as it was not attached to any volume")
        else:
            #check if the volume still exist
            try:
                volume_response = ec2.describe_volumes(VolumeIds=[volume_id])
                if not volume_response['Volumes'][0]['Attachmenta']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
            except ec2.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    #the volume associated with thr snapshot is not found (it might have been deleted)
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f"Delete EBS snapshot {snapshot_id} as it's associated volume was not found")
                    
