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
- 

## Suggested implementation
You can update any part of code, but  and filenames should look like 
- Cloud provider as you already guessed - AWS.
- Use free tier instances obviously because they are free.
- To easily create instances with proxy pre-installed you can create AMI images based on free-tier images. 
- I suggest you to use "boto3" library for python or any you want.
- 


![With Proxy](https://drive.google.com/uc?export=view&id=1ZukJEYE1tOnkU0NoiNLdDmu_Ta2e7WGE)
![AWS algo 1](https://drive.google.com/uc?export=view&id=1gLNwFjlm9X-873mtVZ8l7EWhWZE6pMYk)
![AWS algo 2](https://drive.google.com/uc?export=view&id=1UI7FhJqrdOqLP-si8tZeGjEfQokuMmtp)
![AWS algo 3](https://drive.google.com/uc?export=view&id=1DUwTYexnfWUxHPkyB-A2xarrf3Rrc8k2)
![AWS algo 4](https://drive.google.com/uc?export=view&id=1M-EhgG7sRLkez2chdId32zrdjN2DwDLH)