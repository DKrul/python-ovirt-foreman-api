#! /usr/bin/python

# Created by Fabian van der Hoeven

#this script requires ovirt-engine-sdk-python
from foreman.client import Foreman
import sys

def connectToHost(host, host_user, host_pwd):
    apiurl="http://"+host
    #insecure -> skips SSL check
    api = Foreman(apiurl, (host_user, host_pwd), api_version=2)
    return api

def createGuest(api, guest_name, guest_hostgroup, guest_domain, guest_organization, guest_location, guest_mac_address, guest_subnet, guest_build='false'):
    guest_hostgroup_id = getHostgroupId(api, guest_hostgroup)
    if guest_hostgroup_id == 0:
        print "Hostgroup '%s' not found. Cannot continue" % guest_hostgroup
        sys.exit(1)
    guest_domain_id = getDomainId(api, guest_domain)
    if guest_domain_id == 0:
        print "Domain '%s' not found. Cannot continue" % guest_domain
        sys.exit(1)
    guest_organization_id = getOrganizationId(api, guest_organization)
    if guest_organization_id == 0:
        print "Organization '%s' not found. Cannot continue" % guest_organization
        sys.exit(1)
    guest_location_id = getLocationId(api, guest_location)
    if guest_location_id == 0:
        print "Location '%s' not found. Cannot continue" % guest_location
        sys.exit(1)
    guest_subnet_id = getSubnetId(api, guest_subnet)
    if guest_subnet_id == 0:
        print "Subnet '%s' not found. Cannot continue" % guest_subnet
        sys.exit(1)

    # Kan middels python api geen organizations ophalen. Kan wel handmatig: http://<foreman_url>/api/organizations
#    guest={'name': guest_name, 'mac': guest_mac_address, 'hostgroup_id': guest_hostgroup_id, 'build': guest_build, 'domain_id': guest_domain_id, 'organization_id': guest_organization_id, 'location_id': guest_location_id, 'subnet_id': guest_subnet_id}
    try:
#        api.hosts.create(host=guest)
        hosts = api.hosts.index()['results']
        api.hosts.create(host={'name': guest_name, 'mac': guest_mac_address, 'hostgroup_id': guest_hostgroup_id, 'build': guest_build, 'domain_id': guest_domain_id, 'organization_id': guest_organization_id, 'location_id': guest_location_id, 'subnet_id': guest_subnet_id})
        result = "Succesfully created guest: " + guest_name
    except Exception as e:
        result = 'Failed to create hoest in Foreman: %s' % str(e)

    return result

def getHostgroupId(api, hostgroupName):
    hostgroups = api.index_hostgroups()['results']
    for hostgroup in hostgroups:
        if hostgroup['name'] == hostgroupName:
            hostgroupId = hostgroup['id']
            break
        else:
            hostgroupId = 0
    return hostgroupId

def getDomainId(api, domainName):
    domains = api.index_domains()['results']
    for domain in domains:
        if domain['name'] == domainName:
            domainId = domain['id']
            break
        else:
            domainId = 0
    return domainId

def getOrganizationId(api, organizationName):
    # Kan middels python api geen organizations ophalen. Kan wel handmatig: http://<foreman_url>/api/organizations, dus hier maar met een dictionary
    organizations = []
    organization = {}
    organization['id'] = 3
    organization['name'] = 'CMC'
    organizations.append(organization)

    for organization in organizations:
        if organization['name'] == organizationName:
            organizationId = organization['id']
            break
        else:
            organizationId = 0
    return organizationId

def getLocationId(api, locationName):
    locations = api.index_locations()['results']
    for location in locations:
        if location['name'] == locationName:
            locationId = location['id']
            break
        else:
            locationId = 0
    return locationId

def getSubnetId(api, subnetName):
    subnets = api.index_subnets()['results']
    for subnet in subnets:
        if subnet['name'] == subnetName:
            subnetId = subnet['id']
            break
        else:
            subnetId = 0
    return subnetId