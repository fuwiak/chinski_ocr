import numpy as np
import requests
from io import BytesIO
import json
import ast
import easyocr
from PIL import Image
import numpy as np
import numpy as np
from PIL import Image
from typing import List, Dict
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def load_content_from_file(path):
    with open(path, 'r') as f:
        try:
            content = json.load(f)
            content = content.replace('"', '\"""')
            data = ast.literal_eval(content)[0]
        except json.decoder.JSONDecodeError:
            f.seek(0)
            content = f.read()
            content = content.replace('"', '\"""')
            data = ast.literal_eval(content)[0]
    return data


def get_attachment_url(data):
    attachment = None
    for line in data:
        if 'attachment' in line and line['attachment'] != '':
            attachment = line['attachment'].replace('\n', '')
    return attachment

def download_image(url, retries=3):
    for _ in range(retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Image.open(BytesIO(response.content))
        except (requests.HTTPError, requests.ConnectionError) as e:
            logging.error(f"Error downloading image, retrying... ({str(e)})")
            print(f"Error downloading image, retrying... ({str(e)})")
    raise Exception(f"Failed to download image after {retries} attempts.")

def extract_text_from_image(img: Image, languages: List[str] = ['ch_sim', 'en'], use_gpu: bool = False) -> str:
    reader = easyocr.Reader(languages, gpu=use_gpu)
    result = reader.readtext(np.array(img))
    extracted_text = [item[1] for item in result]
    text = ' '.join(extracted_text)
    return text


def format_string_into_role_based_format(data: str) -> dict:
    formatted_data = []
    inner_list = []

    roles = ["<用户>", "<客服>"]
    split_data = data.split(" ")

    for i, word in enumerate(split_data):
        role = roles[i % 2]
        message = word
        inner_dict = {
            "role": role,
            "attachment": "",
            "message": message
        }
        inner_list.append(inner_dict)

    formatted_data.append(inner_list)

    return formatted_data

def transform_dialogues(data: List[List[Dict[str, str]]]) -> List[str]:
    simplified_dialogues = []

    for dialogue in data:
        simplified_dialogue = ""
        for message in dialogue:
            role = message['role']
            text = message['message']
            simplified_dialogue += f"{role} {text}\n"

        simplified_dialogues.append(simplified_dialogue.strip())

    return simplified_dialogues





if __name__ == '__main__':
    try:
        path = 'sample_json.txt'
        data = load_content_from_file(path)
        logging.info('Loaded data from file.')
        attachment = get_attachment_url(data)
        logging.info('Got attachment URL.')
        img = download_image(attachment)
        logging.info('Downloaded image.')

        text = extract_text_from_image(img)
        formatted_data = format_string_into_role_based_format(text)
        print(transform_dialogues(formatted_data))
        logging.info('Transformation successful.')

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(e)
        img = img.convert('RGB')
        text = extract_text_from_image(img)
        formatted_data = format_string_into_role_based_format(text)
        print(transform_dialogues(formatted_data))
    finally:
        img.close()
        logging.info("Done!")
