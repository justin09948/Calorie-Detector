import torch
from torchvision import models, transforms
from PIL import Image
import cv2
import numpy as np
import pytesseract
import requests

def caloriesCount(image_file):
    model = models.resnet50(pretrained = False)
    model.fc = torch.nn.Linear(model.fc.in_features, 101)
    model.load_state_dict(torch.load("C:\\Users\\Justin\\Documents\\Projects Coding\\Calorie Detection\\backend\\ML\\best_model.pth"))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = Image.open(image_file)
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image_tensor)

    _, prediction = output.max(1)

    with open("C:\\Users\\Justin\\Documents\\Projects Coding\\Calorie Detection\\backend\\ML\\data\\food101\\meta\\classes.txt", "r") as f:
        class_names = [line.strip() for line in f.readlines()]
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
     
    image = np.array(image)
    cropped_image = image[4750:5270, 2500:3750]
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blurred, 135, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((9, 9), np.uint8)
    dilated_image = cv2.dilate(threshold, kernel, iterations=1)
    kernel = np.ones((7,7),np.uint8)
    eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
    weight = pytesseract.image_to_string(eroded_image, lang='lets', config='--psm 6')

    api_id = "a94b99e8"
    api_key = "5d3e5bf72ba94b3709540349fb50ff7c"
    api_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

    food_input = f"{class_names[prediction.item()]} {int(float(weight))}g"

    headers = {
        "x-app-id": api_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "query": food_input,
        "timezone": "US/Eastern"
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        food = data["foods"][0]
        return(food['food_name'], food.get('nf_calories', 'N/A'), food.get('nf_protein', 'N/A'))