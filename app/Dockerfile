FROM public.ecr.aws/lambda/python:3.8

ADD app.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD resnet34.pt ./
ADD imagenet_classes.txt ./

CMD ["app.lambda_handler"]