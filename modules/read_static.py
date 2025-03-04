import json, os, aiogram.types

def read_json(file_name):
    file_path = os.path.abspath(__file__+f'/../../static/tests/{file_name}.json')
    with open(file_path,'r', encoding='utf-8') as file:
        return json.load(file)
    
def get_image(image_name):
    image_path = os.path.abspath(__file__+f'/../../static/images/{image_name}')
    return aiogram.types.FSInputFile(image_path)