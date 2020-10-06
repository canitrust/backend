import json
import os
import sys

BASE_PATH = os.path.abspath(os.path.dirname(__file__) + '/../../driver/config/')
DES_PATH = '%s/description'%BASE_PATH
MAP_FILE = '%s/map.json'%BASE_PATH
TAGS_FILE = '%s/tags.json'%BASE_PATH
TESTCASES_FILE = '%s/testcases.json'%BASE_PATH

with open(MAP_FILE) as jsonMapFile, open(TAGS_FILE) as jsonTagsFile, open(TESTCASES_FILE) as jsonTestcasesFile:
  jsonMap = json.load(jsonMapFile)
  jsonTags = json.load(jsonTagsFile)
  jsonTestcases = json.load(jsonTestcasesFile)

  # For each test case in map.json that is set to "isLive": true, the corresponding test case content from testcases.json is synced to the staging database
  testcases = []
  for testNumber in jsonMap:
    if jsonMap[testNumber]['isLive']:
      if testNumber in jsonTestcases:
        try:
          with open('%s/%s.md'%(DES_PATH, testNumber)) as detailedDescriptionFile:
            jsonTestcases[testNumber]['detailedDescription'] = detailedDescriptionFile.read()
        except Exception as e:
          print('Error: No detailed description markdown file for testcase number %s' % testNumber)
          sys.exit(1)
        print('Extract testcase number %s' % testNumber)
        testcases.append(jsonTestcases[testNumber])
      else:
        print('Error: No description for testcase number %s' % testNumber)
        sys.exit(1)

  # Write tags to json array file
  with open('testcases.db.json', 'w') as testcasesOutFile:
    json.dump(testcases, testcasesOutFile)

  # All tags in tags.json are synced to the staging database
  tags = []
  for tagNumber in jsonTags:
    print('Extract tag number %s' % tagNumber)
    tags.append(jsonTags[tagNumber])

  # Write tags to json array file
  with open('tags.db.json', 'w') as tagsOutFile:
    json.dump(tags, tagsOutFile)
