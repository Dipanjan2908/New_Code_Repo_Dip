#This module contains all the functions and variables related to report generation
#Created By : Dipanjan Roy
#Created Dt : 09-05-2020
#Version No : v1.0



import subprocess as sp
from datetime import datetime
import os
import json


# The common variables for this module

temp = 'DEVSHELL_PROJECT_ID'
project = os.getenv(temp)
print("Project :",project)

dateTimeObj = datetime.now()
timestampStra = dateTimeObj.strftime("%Y-%m-%dT%H:%M:%SZ")
timestampStr = dateTimeObj.strftime("%Y-%m-%dT00:00:00Z")
print("current timstamp :",timestampStr,"\n")

def bucketInfo():

#The dynamic generation of command

    cmd1 = 'gcloud beta logging read \'resource.type="gcs_bucket" AND resource.labels.project_id="{}" AND protoPayload.methodName="storage.buckets.create" AND timestamp<"{}"\' --format=json'.format(project,timestampStr)
    print(cmd1)
    cmd2 = 'gcloud beta logging read \'resource.type="gcs_bucket" AND resource.labels.project_id="{}" AND protoPayload.methodName="storage.buckets.create" AND timestamp<="{}"\' --format=json'.format(project,timestampStra)
    print(cmd2)
    cmd3 = 'gcloud beta logging read \'resource.type="gcs_bucket" AND resource.labels.project_id="{}" AND protoPayload.methodName="storage.buckets.delete" AND timestamp>"{}"\' --format=json'.format(project,timestampStr)
    print(cmd3)

#The execution of the command 1 begins ----

    rst1 = sp.run(cmd1, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    assert rst1.returncode == 0, rst1.stderr.decode("utf-8")
    output1 = rst1.stdout.decode("utf-8")
    parsedata1 = json.loads(output1)

#The execution of the command 2 begins ----

    rst2 = sp.run(cmd2, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    assert rst2.returncode == 0, rst2.stderr.decode("utf-8")
    output2 = rst2.stdout.decode("utf-8")
    parsedata2 = json.loads(output2)

#The execution of the command 2 begins ----

    rst3 = sp.run(cmd3, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    assert rst3.returncode == 0, rst2.stderr.decode("utf-8")
    output3 = rst3.stdout.decode("utf-8")
    parsedata3 = json.loads(output3)



    yield parsedata1
    yield parsedata2
    yield parsedata3
