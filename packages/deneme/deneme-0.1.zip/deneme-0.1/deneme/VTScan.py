import os
try:
    import requests
except ImportError:
    os.system("pip3 install requests")
    os.system("cls")
    import requests
class VTScan:
    def __init__(self):
        self.API_KEY = "f960e86374a177fa935f52c5063269a6710f5e9f0a1efcd5fb2853f2f3167865"
        self.params = {'apikey': self.API_KEY}
        self.resource = ""
        self.DETECTED_TRUE = []
        self.DETECTED_FALSE = []

    def fileScan(self, filename = ""):
        files = {'file':  open(filename, 'rb')}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=self.params)
        json_response = response.json()
        resource = json_response.get("resource")
        self.resource += resource
    
    def zipScan(self, zipname):
        files = {"type":"bundle",'file':open(zipname, 'rb')}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=self.params)
        json_response = response.json()
        resource = json_response.get("resource")
        self.resource += resource

    def urlScan(self,url):
        self.params["resource"] = url
        response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=self.params)
        json_response = response.json()
        malwareCompaines = json_response.get("scans")
        for company in malwareCompaines:
            reportDetail = malwareCompaines.get(company)
            if reportDetail.get("detected") == False:
                self.DETECTED_FALSE.append({"company":company, "detected":"No Malware"})
            else:
                self.DETECTED_TRUE.append({"company":company, "detected" : "Yes Malware"})
        return [self.DETECTED_TRUE, self.DETECTED_FALSE]

    def Report(self):
        resourceCode = self.resource
        self.params['resource'] = resourceCode
        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Dont Connection with virustotal.com")
        json_response = response.json()
        malwareCompaines = json_response.get("scans")
        return malwareCompaines

    def MalwareDetect(self):
        malwareCompanies = self.Report()
        for company in malwareCompanies:
            reportDetail = malwareCompanies.get(company)
            if reportDetail.get("detected") == False:
                self.DETECTED_FALSE.append({"company":company, "detected":"No Malware"})
            else:
                self.DETECTED_TRUE.append({"company":company, "detected" : "Yes Malware"})
        return [self.DETECTED_TRUE, self.DETECTED_FALSE]

