import xmltodict
import json
file = (input("Please enter your file name (without .xml): "))

try:
    with open(file + ".xml", 'r') as xml:
        # parse xml to dict
        dict = xmltodict.parse(xml.read())
        # create file 'data.json'
        with open(file + ".json", 'w') as file:
            # parse dict to json
            # replace prefix in dict before write
            file.write(json.dumps(dict).replace('@', ''))
            print("success")
except:
    print("can't find xml file")

# prevent from closing immediately
input("\nPress enter to close program")
