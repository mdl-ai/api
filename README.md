# MDL.AI API

## Purpose
This project is open source so it can be used as a learning resource for others as I find the cheapest methods possible for deploying machine learning models, currently I'm using Lambda to start a docker container so it can remain within free tier on AWS.

## Cold starts
Once the docker container is running latency is excellent (double digit millisecond), however it has a long 'cold start' time while it pulls the docker image down, if left idle for over 45 minutes it will dissapear from the cache leaving a user with a long 'cold-start' time again.

## Provisioned Lambda
You can now provision lambdas to always be active, in addition to starting new ones when required. This effectively removes the cold start issue and completely negates the only weakness of running docker containers in Lambdas. It used to be a trade off deciding between container based services like Kubernetes / Fargate or serverless architechtures, I think this methodolgy will quickly become the standard as more people become aware of the benefits.

## Fast API
Fast API is great for fast development and quick debugging, I've been experimenting with using API Gateway as a proxy to the Lambda, and having FastAPI deal with all the routing inside the Lambda.

This is an excellent developer experience as you can quickly iterate locally, then upload to the cloud with the addition of two lines of code to use the Mangum package. This offers much faster iteration than debugging Lambda functions inside the AWS docker containers, which take quite a while to start up.

## Future Dev
As I learn more about machine learning I'll be deploying my inference models from here, the CI/CD offered with SAM is very good.
Next step is to convert the models to C++ for production deployment.
