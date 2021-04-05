import json
import io
import urllib
import torch
from PIL import Image
from torchvision import transforms
import base64

transform_test = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def lambda_handler(event, context):
    # If recieving an image url
    body = json.loads(event["body"])
    if ("url" in body):
        img = Image.open(urllib.request.urlopen(body["url"]))

    # If recieving binary data
    if ("data" in body):
        data = body["data"].split(',')[1]
        data = bytes(data, 'utf-8')
        img = base64.decodebytes(data)
        img = Image.open(io.BytesIO(img)).convert('RGB')
        # img = Image.frombytes('RGB', (500, 500), img, 'raw')

    scaled_img = transform_test(img)
    torch_image = scaled_img.unsqueeze(0)
    model = torch.jit.load('./resnet34.pt')
    predicted_class = model(torch_image).argmax().item()
    print('predicted_class: {}'.format(predicted_class))

    # Read the categories
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    print('Categories count: {}'.format(len(categories)))
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-credentials': 'True',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        'body': json.dumps(categories[predicted_class])
    }