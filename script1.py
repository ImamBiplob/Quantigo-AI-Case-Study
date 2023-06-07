import json
import glob
from pathlib import Path

files = glob.glob("./*.json")

for file in files:
    standardFormat = [
        {
            "dataset_name": "",
            "image_link": "",
            "annotation_type": "image",
            "annotation_objects": {
                "vehicle": {
                    "presence": 0,
                    "bbox": []
                },
                "license_plate": {
                    "presence": 0,
                    "bbox": []
                }
            },
            "annotation_attributes": {
                "vehicle": {
                    "Type": None,
                    "Pose": None,
                    "Model": None,
                    "Make": None,
                    "Color": None
                },
                "license_plate": {
                    "Difficulty Score": None,
                    "Value": None,
                    "Occlusion": None
                }
            }
        }
    ]

    fileName = file[2:]
    file = Path(fileName).read_text()
    data = json.loads(file)

    standardFormat[0]["dataset_name"] = fileName

    if (len(data["objects"]) == 0):
        standardData = json.dumps(standardFormat)
        Path(
            f"./Formatted Files/formatted_{fileName}").write_text(standardData)

    elif data["objects"][0]["classTitle"] == "Vehicle":
        standardFormat[0]["annotation_objects"]["vehicle"]["presence"] = 1
        standardFormat[0]["annotation_objects"]["vehicle"]["bbox"] = data["objects"][0]["points"]["exterior"][0] + \
            data["objects"][0]["points"]["exterior"][1]
        standardFormat[0]["annotation_attributes"]["vehicle"]["Type"] = data["objects"][0]["tags"][0]["value"]
        standardFormat[0]["annotation_attributes"]["vehicle"]["Pose"] = data["objects"][0]["tags"][1]["value"]
        standardFormat[0]["annotation_attributes"]["vehicle"]["Model"] = data["objects"][0]["tags"][2]["value"]
        standardFormat[0]["annotation_attributes"]["vehicle"]["Make"] = data["objects"][0]["tags"][3]["value"]
        standardFormat[0]["annotation_attributes"]["vehicle"]["Color"] = data["objects"][0]["tags"][4]["value"]

        if (len(data["objects"]) < 2):
            standardFormat[0]["annotation_attributes"]["license_plate"]["Occlusion"] = 1
        elif data["objects"][1]["classTitle"] == "License Plate":
            standardFormat[0]["annotation_objects"]["license_plate"]["presence"] = 1
            standardFormat[0]["annotation_objects"]["license_plate"]["bbox"] = data["objects"][1]["points"]["exterior"][0] + \
                data["objects"][1]["points"]["exterior"][1]
            standardFormat[0]["annotation_attributes"]["license_plate"]["Difficulty Score"] = data["objects"][1]["tags"][0]["value"]
            standardFormat[0]["annotation_attributes"]["license_plate"]["Value"] = data["objects"][1]["tags"][1]["value"]
            standardFormat[0]["annotation_attributes"]["license_plate"]["Occlusion"] = 0

        standardData = json.dumps(standardFormat)
        Path(
            f"./Formatted Files/formatted_{fileName}").write_text(standardData)
