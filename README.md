# Junior Python developer test task (AWS)
![python3](https://img.shields.io/badge/-python3-yellowgreen)
![rabbit](https://img.shields.io/badge/-RabbitMQ-green)
![docker](https://img.shields.io/badge/-Docker-orange)
![AWS](https://img.shields.io/badge/-AWS-brightgreen)
## Helpful links
To submit your application, please put your results into this [form](https://forms.gle/hLrkZvZDVFkBG7Wy6)
Feel free to ask questions [here](https://app.sli.do/event/es9DAm5Y8SipuNvhzqp96Q/live/questions)
## Overiview
This repository is an example of how to download 100k [tiles](https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/#1/180.00/-46.60) (or any other amount) from Google tile server. 
Key point here is that it uses Message Broker (RabbitMQ) for passing messages between processes.

We have 3 main components here:
1. Message generator
2. Message Broker
3. Message consumer

*Message generator* creates messages with enough information to create a link and download the file.
Later after consumer sees the message it takes it from the queue and downloads the image.
This way we can easily specify in *docker-compose replicas: N*, and there will be as many "downloaders" as you want.
This solution works perfectly, but some services does not allow to download too much data from their servers, usually they ban by IP.
The goal is to update current soluton to be able to send requests using different IP addresses so requests won't be blocked.

This is how it looks like for now:
![No Proxy](https://drive.google.com/uc?export=view&id=1QFR_e1rh5Ao0BVwEjvROfsGqa0zWogy7)

## General implementation idea
To have another public IP in requests we can create instances in cloud like AWS.
Each instance created by AWS will have differenet public IP.
We will create instances on AWS with proxy pre-installed (it can be "mitm-proxy", or any other you like) and then we can connect from our consumers to them.

## Requirements
Please, make sure your code follows these requirements in other way solution won't be evaluated
- Solution should work just right after I pull repo with code. (Write needed .sh scripts, or requirements.txt etc. ...)
- Cloud provider as you already guessed - AWS.
- Images should to be saved in './tiles'
- Filenames format should be "\<x\>\_\<y\>\_\<zoom\>.png"
- Solution should switch to another proxy instance either after 5 minutes or after getting ERROR 403 (forbidden).
- There are no pre-created instances in AWS, you have to create them by your own using python library for automation
- After your solution finishes working it should remove any resources created in AWS
- You have to use git as version control system and store your repo in Github or any other similar system. The easiest way to start working on the task is to [fork](https://github.com/zakhar-bozhok-jito/jun-python-aws-test-task/fork) this repo.
- Solution should work with more than one replicas of client i.e. multiprocess solution
- Add enough logging to understand key events like proxy switching, errors, warning, etc., make reviewer experience as easy as possible to understand what is happening with your program.
- Use env variables to connect to AWS (AWS_SERVER_PUBLIC_KEY, AWS_SERVER_SECRET_KEY) like in [example](https://stackoverflow.com/questions/45981950/how-to-specify-credentials-when-connecting-to-boto3-s3)

## What will be checked during test task evaluation?
- Solution should correspond to requirements
- Understanding and usage of [SOLID](https://en.wikipedia.org/wiki/SOLID)
- Understanding and usage of [OOP](https://en.wikipedia.org/wiki/Object-oriented_programming) or FP
- [Code style consistency](https://blog.devgenius.io/why-code-consistency-is-important-9d95bdebcef4)
- Code readability and [cognitive complexity](https://docs.codeclimate.com/docs/cognitive-complexity#:~:text=Cognitive%20Complexity%20is%20a%20measure,be%20to%20read%20and%20understand.)
- Efficiency of solution
- Clean git history with understandable commit messages

## Suggested implementation
You can update any part of code
- Use free tier instances on AWS. Obviously because they are free.
- To easily create instances with proxy pre-installed you can create AMI images based on free-tier images. 
- I suggest you to use "boto3" library for python or any you want.
- To pass info to downloaders I suggest you to use already existing RabbitMQ, and in generatl read more about AMQP and related topics.
- How in my opnionion your solution shoud look like
![With Proxy](https://drive.google.com/uc?export=view&id=1ZukJEYE1tOnkU0NoiNLdDmu_Ta2e7WGE)
- Algorithm of switching the proxies:
1. At the beginning we have 2 proxy instances created, and traffic is proxified only by instance A
![AWS algo 1](https://drive.google.com/uc?export=view&id=1gLNwFjlm9X-873mtVZ8l7EWhWZE6pMYk)
2. After either 5 minutes passes or we receive 403 we switch proxifying to instance B and during that we terminate proxy instance A and booting up instance C
![AWS algo 2](https://drive.google.com/uc?export=view&id=1UI7FhJqrdOqLP-si8tZeGjEfQokuMmtp)
3. Instance C has already booted, but we still proxifying using instance B.
![AWS algo 3](https://drive.google.com/uc?export=view&id=1DUwTYexnfWUxHPkyB-A2xarrf3Rrc8k2)
4. And after 5 minutes passes or we receive 403 we switch proxifying to instance C, and during that terminating instance B and creating another instance instead of B, for example D. And the algorithm repeats from step 1 till all images are downloaded. 

![AWS algo 4](https://drive.google.com/uc?export=view&id=1M-EhgG7sRLkez2chdId32zrdjN2DwDLH)