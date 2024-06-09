import os
from pathlib import Path
from openai import OpenAI
import io
from pydub import AudioSegment
from pydub.playback import play
import requests
import json
import cv2
import time

#plantnet
plantnet_api_key = os.environ.get('PlantNet_API_KEY')
PROJECT = "japan"; # try specific floras: "weurope", "canada"…
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={plantnet_api_key}"
# output_file_path = "/content/output.json"

def capture_image_from__camera():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("failed to capture image")
        return
    image_path = "temp.jpg"
    cv2.imwrite(image_path, frame)
    cap.release()
    # cv2.destroyAllWindows()
    return image_path

def get_result_from_api(image_path):
    image_data = open(image_path, 'rb')
    data = {
    # 'organs': ['flower', 'leaf'],
    'organs': ['leaf']
    }
    files = [
    ('images', (image_path, image_data)),
    # ('images', (image_path_2, image_data_2))
    ]
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    # print(json_result)

    if response.status_code != 200:
        return None, None
    if json_result['results'][0]['score'] > 0.25:
        top_candidates = [json_result['results'][0]]
    else:
        top_candidates = json_result['results'][:4]
    simplified_json = {
        "top_candidates": [
            {
                "scientific_name": candidate['species']['scientificNameWithoutAuthor'],
                "common_names": candidate['species']['commonNames'],
                "score": candidate['score'],
                "genus": candidate['species']['genus']['scientificNameWithoutAuthor'],
                "family": candidate['species']['family']['scientificNameWithoutAuthor'],
            } for candidate in top_candidates
        ]
    }

    # with open(output_file_path, 'w') as file:
    #     json.dump(simplified_json, file, indent=4)
    
    return response, simplified_json
