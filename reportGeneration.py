# This application is actualy used for generation of report related to different services of GCP

import reportInfo as ri
import csv
import pandas as pd
import matplotlib_venn as vpit
from matplotlib_venn import venn2_unweighted
import matplotlib
import base64
# The main processing starts from here 
if __name__ == "__main__":
    
    parsedata = ri.bucketInfo()
    parsedataB = parsedata.__next__()
    parsedataA = parsedata.__next__()
    parsedataD = parsedata.__next__()
    bucket_header = ["Bucket_Creator","Create_Time","Bucket_Name","Bucket_Location"]
    
    bucket_creatorB = []
    bucket_create_timeB = []
    bucket_nameB = []
    bucket_locationB = []

    for item in parsedataB:
       bucket_creatorB.append(item['protoPayload']['authenticationInfo']['principalEmail'])
       bucket_create_timeB.append(item['receiveTimestamp'])
       bucket_nameB.append(item['resource']['labels']['bucket_name'])
       bucket_locationB.append(item['resource']['labels']['location'])

    bucket_detailsB = pd.DataFrame({"Bucket_Name":bucket_nameB,"Bucket_creator":bucket_creatorB,"Bucket_Create_Time":bucket_create_timeB,"Bucket_Location":bucket_locationB})
    print(bucket_detailsB)
    
    bucket_creatorA = []
    bucket_create_timeA = []
    bucket_nameA = []
    bucket_locationA = []
    
    for item in parsedataA:
       bucket_creatorA.append(item['protoPayload']['authenticationInfo']['principalEmail'])
       bucket_create_timeA.append(item['receiveTimestamp'])
       bucket_nameA.append(item['resource']['labels']['bucket_name'])
       bucket_locationA.append(item['resource']['labels']['location'])

    bucket_detailsA = pd.DataFrame({"Bucket_Name":bucket_nameA,"Bucket_creator":bucket_creatorA,"Bucket_Create_Time":bucket_create_timeA,"Bucket_Location":bucket_locationA})
    print(bucket_detailsA)

    
    bucket_creatorD = []
    bucket_create_timeD = []
    bucket_nameD = []
    bucket_locationD = []
    
    for item in parsedataD:
       bucket_creatorD.append(item['protoPayload']['authenticationInfo']['principalEmail'])
       bucket_create_timeD.append(item['receiveTimestamp'])
       bucket_nameD.append(item['resource']['labels']['bucket_name'])
       bucket_locationD.append(item['resource']['labels']['location'])

    bucket_detailsD = pd.DataFrame({"Bucket_Name":bucket_nameD,"Bucket_creator":bucket_creatorD,"Bucket_Create_Time":bucket_create_timeD,"Bucket_Location":bucket_locationD})
    print(bucket_detailsD)

    
    bucketAB = bucket_detailsB.merge(bucket_detailsA,how = "outer",on = "Bucket_Name",indicator = True)
    print(bucketAB)
    New_Bucket = bucketAB.loc[bucketAB._merge == "right_only"].iloc[:,[0,4,5,6]]
    New_Bucket.columns = bucket_header
    print(New_Bucket)

    v=vpit.venn2_unweighted(subsets={"10":len(bucket_detailsB.index),'01':len(New_Bucket.index),'11':len(bucket_detailsD.index)},set_labels=('Before','New'),alpha=0.5)
    matplotlib.pyplot.savefig("temp.png")
    data_uri = base64.b64encode(open('temp.png','rb').read()).decode('utf-8')
    venn_image = '<img src="data:image/png;base64,{0}">'.format(data_uri)


    HEADER ="""
    <html>
    <head>
    <style>


    .panel{margin-bottom20px;background-color:#fff;border:3px solid;border-radius;border-color:#1f0f66;}
    .panel-body{margin: 30px;}
    .panel-heading{padding:20px 20px;color:#fff:background-color:#1f0f66;border-color:#F71515;}
    table{border: 1px solid black;border-collapse: collapse;margin:1px;style="width:100%"}
    tr.th.td{border: 1px solid black:border-collapse:collapse;padding:15px;font-size: 5px;font-weight: lighter;}
    th{background-color:#add2f0;text-align:left;}
    </style>
    </head>
    <div class="panel">
    """

    with open("mail_body.html","w") as f:
        f.write(HEADER)
        f.write("<h3>BUCKET STATUS BEFORE CRQ</h3>")
        f.write(bucket_detailsB.to_html(index=False))
        f.write("<hr>")
        f.write("<h3>Newly added buckets</h3>")
        f.write(New_Bucket.to_html(index=False))
        f.write("<hr>")
        f.write("<h3>Deleted Bucket Details</h3>")
        f.write(bucket_detailsD.to_html(index=False))
        f.write("<hr>")
        f.write(venn_image)
        f.write("</html>")
    

    
    
    
