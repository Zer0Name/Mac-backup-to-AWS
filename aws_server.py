from boto import ec2
import boto
import time
from boto.ec2.connection import EC2Connection
from boto.ec2.blockdevicemapping import BlockDeviceType, BlockDeviceMapping

    
class server:
    
    # access key
    # secret access key 
    # size is in GB 
    # name of software : ami-fce3c696 
    # key_name: the name of the key to access the server 
    # instance_type the type of instance
    # security_groups the security_groups for the server 
    # user_data the code that will run when the server starts up 
    
    def __init__(self, aws_access_key_id, aws_secret_access_key,size , name,key_name, instance_type, security_groups, user_data  ):
        
        #creates the external storage 
        dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType(delete_on_termination=True)
        dev_sda1.size = size # size in Gigabytes
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1 
        
        #connectts the aws 
        conn = ec2.connection.EC2Connection(aws_access_key_id, aws_secret_access_key)
        
        #starts server
        reservation = conn.run_instances(name ,key_name= key_name ,instance_type=instance_type, security_groups = security_groups , user_data = user_data, block_device_map=bdm)      
        
        print "lunching instance"
        
        
        # instance = reservation.instances[0]
        # while instance.state != 'running':
        #     print '...instance is %s' % instance.state
        #     time.sleep(2)
        #     instance.update()
        
        
    
