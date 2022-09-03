# Junior Python developer test task (with AWS direction)
## Overiview
This repository is an example of how to download 100k [tiles](https://www.maptiler.com/google-maps-coordinates-tile-bounds-projection/#1/180.00/-46.60) (or any other amount) from Google tile server. 
Key point here is that it uses Message Broker (RabbitMQ) for passing messages between processes.

We have 3 main components here:
1. Message generator
2. Message Broker
3. Message consumer

*Message generator* creates messages with enough information to create a link and download the file.
Later after consumer sees the message it takes it from the queue and downloads the image.
This way wee can easily specify in *docker-compose replicas: N*, and there will be as many "downloaders" as you want.
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
- Cloud provider as you already guessed - AWS.
- Images should to be saved in './tiles'
- Filenames format should be "\<x\>\_\<y\>\_\<zoom\>.png"
- Solution should switch to another proxy instance either after 5 minutes or after getting ERROR 403 (forbidden).
- There are no pre-created instances in AWS, you have to create them by your own using python library for automation
- After your solution finishes working it should remove any resources created in AWS
- You have to use git as version control system and store your repo in Github or any other similar system. The easiest way to start workong on the task is to [fork](https://github.com/zakhar-bozhok-jito/jun-python-aws-test-task/fork) this repo. 

## Suggested implementation
You can update any part of code, but  and filenames should look like 
- Use free tier instances obviously because they are free.
- To easily create instances with proxy pre-installed you can create AMI images based on free-tier images. 
- I suggest you to use "boto3" library for python or any you want.
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