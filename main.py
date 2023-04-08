import requests
from pathlib import Path
import os
import shutil
from bs4 import BeautifulSoup
import zipfile

# Enter the data report url here
report_page_url="https://www.ercot.com/mp/data-products/data-product-details?id=NP4-180-ER"


page =requests.get(report_page_url)
baseurl= 'https://www.ercot.com/'
soup = BeautifulSoup(page.content, "lxml")
soup.prettify()

report_type_id = soup.find(text="Report Type ID").findNext('span').contents[0]
endpoint = f"https://www.ercot.com/misapp/servlets/" \
           f"IceDocListJsonWS?reportTypeId="+str(report_type_id)+"&_={int(time.time())}"
headers = {
  'Cookie': 'incap_ses_387_1217363=ZUTJFIw3mRfr97jxaedeBdBOMGQAAAAA82UmLPJUC0IraVm3FYEU/Q==; visid_incap_1217363=uchpJRtSTnmlCstiBm7YNrdLMGQAAAAAQUIPAAAAAABdYpeW+PPmCTxFcCagj8ov'
}
download_url = "https://www.ercot.com/misdownload/servlets/mirDownload?doclookupId="

# create directory to store data
if(os.path.isdir('data')):
    shutil.rmtree("data")
if(os.path.isdir('extract_data')):
    shutil.rmtree("extract_data")
os.makedirs("data", exist_ok=True)
os.makedirs("extract_data", exist_ok=True)



auction_results = requests.request("GET",endpoint, headers=headers).json()
i=1
for result in auction_results["ListDocsByRptTypeRes"]["DocumentList"]:
    file_name = result["Document"]["ConstructedName"]
    friendly_name = str(i)+"_"+result['Document']['FriendlyName']+".zip"
    zip_url = f"{download_url}{result['Document']['ReportTypeID']}"
    url = f"{download_url}{result['Document']['DocID']}"
    payload={}
    print("Downloading "+friendly_name)
    payload={}
    response = requests.request("GET", url, headers=headers, data=payload)

    with open(Path("data") / friendly_name,'wb') as output_file:
        output_file.write(response.content)
    i=i+1


# To extract the files
print("Starting unzip files ")
for f_name in os.listdir(os.path.abspath(os.curdir)+"/data"):
    with zipfile.ZipFile((os.path.abspath(os.curdir)+"/data/"+f_name),"r") as zip_ref:
        zip_ref.extractall("extract_data")
print("Download and extraction completed!")



