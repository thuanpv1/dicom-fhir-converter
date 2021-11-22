from datetime import datetime
import os
import json
import copy
import datetime
from dicom2fhir import dicom2fhir
from fhir import resources as fr

def convert_class_to_json(cls):
        try:
            aDict = vars(cls)
        except: 
            if cls == None:
                aDict = None
            elif isinstance(cls, datetime.datetime) == True:
                aDict = cls.strftime('%Y-%m-%d %H:%M:%S')
            else:
                aDict = cls
            print('failed to convert to dict===', cls)
        for x in aDict:
            try:
                if isinstance(aDict[x], list) == True:
                    temp = []
                    for each in aDict[x]:
                        if isinstance(each, str) == True and isinstance(each, int) == True and isinstance(each, float) == True and isinstance(each, complex) == True and isinstance(each, slice) == True:
                            temp.append(each)
                        else:
                            temp.append(convert_class_to_json(each))
                    aDict[x] = temp
                else: 
                    try:
                        aDict[x] = convert_class_to_json(aDict[x])
                    except: 
                        # print('failed to convert to dict x===', x, aDict[x])
                        if aDict[x] == None:
                                aDict[x] = None
                        if isinstance(aDict[x], datetime.datetime) == True:
                            aDict[x] = aDict[x].strftime('%Y-%m-%d %H:%M:%S')
            except:
                try:
                    aDict[x] = convert_class_to_json(aDict[x])
                except: 
                    # print('failed to convert to dict x===', x, aDict[x])
                    if aDict[x] == None:
                            aDict[x] = None
                    if isinstance(aDict[x], datetime.datetime) == True:
                            aDict[x] = aDict[x].strftime('%Y-%m-%d %H:%M:%S')

        return aDict


dcmDir = os.path.join(os.getcwd(), "dicom2fhir", "tests", "resources", "DICOM")
study = dicom2fhir.process_dicom_2_fhir(dcmDir)
# print(study.as_json())
with open ('output.json', 'w') as f:
    json.dump(study.as_json(), f)
# fhirOutput = convert_class_to_json(study)
# print('fhirOutput===', json.dumps(fhirOutput))