#!/usr/bin/env python

from utils import GCPEXCEPTION
from utils import signal_handler
from signal import signal, SIGINT
signal(SIGINT, signal_handler)
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

class GcpIap:

    def __init__(self, SERVICE_ACCOUNT_FILE):
        SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
        try:
            self.credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        except IOError as e:
            raise GCPEXCEPTION(str(e))
        
    def getResource(self, resource, version):
        return build(resource, version, credentials=self.credentials)

    def getProject(self, projectId):
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            return service.projects().get(projectId=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listProjects(self):
        l = []
        service = self.getResource('cloudresourcemanager', 'v1')
        try:
            for project in service.projects().list().execute()['projects']:
                l.append(project['projectId'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getAllInstancesRaw(self, projectId):
        service = self.getResource('compute', 'v1')
        try:
            return service.instances().aggregatedList(project=projectId).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listZonesUsed(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    l.append(k.replace('zones/',''))
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstancesByZone(self, projectId, zone):
        l = []
        service = self.getResource('compute', 'v1')
        try:
            instances = service.instances().list(project=projectId, zone=zone).execute()
            for v in instances['items']:
                l.append(v['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def listInstances(self, projectId):
        l = []
        try:
            instances = self.getAllInstancesRaw(projectId)
            for k,v in instances['items'].items():
                if 'instances' in v:
                    for instance in v['instances']:
                        l.append(instance['name'])
            return l
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def getIapPolicy(self, project, zone=None ,instance=None):
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            return service.v1beta1().getIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance)).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

    def setIapPolicy(self, project, policyfile, zone=None ,instance=None):
        service = self.getResource('iap', 'v1beta1')
        project_num = self.getProject(project)['projectNumber']
        zone = '/zones/%s' % zone if zone else ""
        instance = '/instances/%s' % instance if instance else ""
        try:
            body = open(policyfile).read()
        except IOError as e:
            raise GCPEXCEPTION(str(e))
        try:
            body = json.loads(body)
        except json.decoder.JSONDecodeError as e:
            raise GCPEXCEPTION(str(e))
        try:
            return service.v1beta1().setIamPolicy(resource='projects/%s/iap_tunnel%s%s' % (project_num, zone, instance), body=body).execute()
        except HttpError as e:
            raise GCPEXCEPTION(e._get_reason())

