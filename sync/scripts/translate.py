import sys
import json
import re
import warnings

class Result:
    #A general class for test result, can hold data from backend as well as frontend

    def __init__(self, backendData):
        #Todo: if backendData is empty, throw an error
        self.backendData = backendData

    # @Output: dict object
    def translate(self):
        try:
            browser_ver = float(self.backendData['version'].replace(' beta',''))
        except:
            browser_ver = self.backendData['version']
        translatedData = {
            "testNumber": self.backendData['testCaseNum'],
            "browser": self.backendData['browser'].capitalize(),
            "browserVer": browser_ver,
            "isBeta": self.backendData['isBeta'],
            "result": self.backendData['result'],
            "date_lasttest": self.backendData['date']
        }
        return translatedData

    # @Output: bool
    def isBeta(self):
        if(self.backendData["isBeta"]):
            return True
        if("beta" in self.backendData["version"]):
            self.backendData["isBeta"] = True
            warnings.warn("Found a beta version where isBeta is not set" + json.dumps(self.backendData))
            return True
        return False

    # @Output: (String) version without the beta part
    def getNonBetaVersion(self):
        try:
            return str((re.match('\d+\.\d', self.backendData["version"])).group(0))
        except:
            return False

    # @Output: (Bool) should this result be ignored (eg. Edge insider preview)
    def shouldIgnore(self):
        shouldIgnore = self.backendData["version"] == "insider preview"
        return shouldIgnore

class VersionIdentityList:
    data = {}
    def memorize(self, aResult):
        staticKey = str(aResult.backendData["testCaseNum"]) + aResult.backendData["browser"]
        dynamicValue = aResult.backendData["version"]
        if(staticKey in self.data):
            self.data[staticKey].append(dynamicValue)
        else:
            self.data[staticKey] = [dynamicValue]
    # @Input (Result) probably a result of a beta version
    # @Output (bool): version is found or not
    def find(self, aResult):
        staticKey = str(aResult.backendData["testCaseNum"]) + aResult.backendData["browser"]
        dynamicValue = aResult.getNonBetaVersion()
        try:
            return (dynamicValue in self.data[staticKey])
        except:
            return False

if __name__ == '__main__':
    # Maybe we will need to modulize this file

    # Statistics
    inputEntity = inputIgnored = inputIsBeta = outputNonBeta = outputBeta = outputBetaFilteredOut = 0

    # Readline input file
    with open(sys.argv[1], "r") as inputFile, open("./translated.json","w") as outputFile:
        versionIdentityList = VersionIdentityList()
        betaTempoList = []
        for aLine in inputFile:
            inputEntity += 1
            # instantiate Result obj
            aResult = Result(json.loads(aLine))
            # If the result should be ignored, skip
            if aResult.shouldIgnore():
                inputIgnored += 1
                continue
            if(aResult.isBeta()):
                inputIsBeta += 1
                betaTempoList.append(aResult)
            else:
                outputNonBeta += 1
                versionIdentityList.memorize(aResult)
                outputFile.write(json.dumps(aResult.translate()) + "\n")

        # Process beta versions
        for aBetaResult in betaTempoList:
            if not versionIdentityList.find(aBetaResult):
            # this beta result does has a corresponding non-beta result
                outputBeta += 1
                outputFile.write(json.dumps(aBetaResult.translate()) + "\n")
            else:
                outputBetaFilteredOut +=1

        # Print statistics
        print(f"Input entities: {inputEntity} (ignored (Insider preview): {inputIgnored}, isBeta: {inputIsBeta})")
        print(f"Output: {outputNonBeta + outputBeta}, isBeta filtered out {outputBetaFilteredOut}, non-beta: {outputNonBeta}, isBeta {outputBeta}")
