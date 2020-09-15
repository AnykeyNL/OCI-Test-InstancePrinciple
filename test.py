import oci
import requests

signer = oci.auth.signers.InstancePrincipalsSecurityTokenSigner()

userName = "Instance Principle"

url = "http://169.254.169.254/opc/v1/instance/"
data = requests.get(url).json()

region = data['canonicalRegionName']
compID = data['compartmentId']
instanceID = data['id']

print ("Metadata:")
print ("region: {}".format(region))
print ("compID: {}".format(compID))
print ("instanceID: {}".format(instanceID))

identity = oci.identity.IdentityClient(config={}, signer=signer)
compute = oci.core.ComputeClient(config={}, signer=signer)
network = oci.core.VirtualNetworkClient(config={}, signer=signer)

print ("Getting instance details  - requiring instance-family permissions")
instanceDetails = compute.get_instance(instance_id=instanceID).data
print (instanceDetails)

print ("Getting vnics  - requiring instance-family permissions")
vnics = compute.list_vnic_attachments(compartment_id=compID, instance_id=instanceID).data
print (vnics)

print ("Getting vnic details  - requiring virtual-network-family permissions")
for vnic in vnics:
        vnic_details = network.get_vnic(vnic_id=vnic.vnic_id).data
        print (vnic_details)
