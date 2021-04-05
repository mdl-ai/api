from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import urllib
import torch
import PIL
from torchvision import transforms
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import base64

transform_test = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DogImage(BaseModel):
    url: Optional[str] = None
    data: Optional[str] = None


@app.get("/")
def read_root():
    return {"API statis": "Hello World!"}


@app.post("/breed/")
def predict_breed(dog_image: DogImage):
    # If recieving an image url
    if (dog_image.url):
        print('getting url')
        img = PIL.Image.open(urllib.request.urlopen(dog_image.url))

    # If recieving binary data
    if (dog_image.data):
        print(dog_image.data)
        data = dog_image.data.split(',')[1]
        data = bytes(data, 'utf-8')
        img = base64.decodebytes(data)
        img = PIL.Image.frombytes('RGB', (128, 128), img, 'raw')

    scaled_img = transform_test(img)
    torch_image = scaled_img.unsqueeze(0)
    model = torch.jit.load('./resnet34.pt')
    predicted_class = model(torch_image).argmax().item()
    print('predicted_class: {}'.format(predicted_class))

    # Read the categories
    with open("imagenet_classes.txt", "r") as f:
        categories = [s.strip() for s in f.readlines()]

    print('Categories count: {}'.format(len(categories)))

    return categories[predicted_class]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)