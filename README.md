# MDL.AI API

## Purpose
Experimental for using Lambda to start up a docker container, this was only made possible at the end of 2020.

## Cold starts
Once the docker container is running latency is excellent (double digit millisecond), however it has a long 'cold start' time while it pulls the docker image down, if left idle for over 45 minutes it will dissapear from the cache leaving a user with a long 'cold-start' time again.

There is a fix detailed here to keep the Lambdas warm:

https://aws.amazon.com/blogs/compute/new-for-aws-lambda-predictable-start-up-times-with-provisioned-concurrency/

However I won't be turning it on to keep my costs low.

## Fast API
Fast API is great for fast development and quick debugging, I've been experimenting with using API Gateway as a proxy to the Lambda, and having FastAPI deal with all the routing inside the Lambda.

This is an excellent developer experience as you can quickly iterate locally, then upload to the cloud with the addition of two lines of code to use the Mangum package. This offers much faster iteration than debugging Lambda functions inside the AWS docker containers which take quite a while to start up.

## Future Dev
As I learn more about machine learning I'll be deploying my inference models from here, the CI/CD offered with SAM is very good.
