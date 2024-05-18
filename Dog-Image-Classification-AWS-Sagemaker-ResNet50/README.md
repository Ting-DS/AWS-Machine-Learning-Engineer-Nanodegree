# Image Classification using AWS SageMaker

Use AWS Sagemaker to train a pretrained model that can perform image classification by using the Sagemaker profiling, debugger, hyperparameter tuning and other good ML engineering practices. This can be done on either the provided dog breed classication data set or one of your choice.

## Project Set Up and Installation
Enter AWS through the gateway in the course and open SageMaker Studio. 
Download the starter files.
Download/Make the dataset available. 

## Dataset
The provided dataset is the dogbreed classification dataset which can be found in the classroom.
The project is designed to be dataset independent so if there is a dataset that is more interesting or relevant to your work, you are welcome to use it to complete the project.

### Access
Upload the data to an S3 bucket through the AWS Gateway so that SageMaker has access to the data. 


## Overview of Project Steps

The jupyter notebook "train_and_deploy.ipynb" walks through implementation of Image Classification Machine Learning Model to classify between 133 kinds of dog breeds using dog breed dataset provided by Udacity (https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip)

- We will be using a pretrained Resnet50 model from pytorch vision library.
- We will be adding in two Fully connected Neural network Layers on top of the above Resnet50 model.
- Note: We will be using concepts of Transfer learning and so we will be freezing all the exisiting Convolutional layers in the pretrained resnet50 model and only changing gradients for the tow fully connected layers that we have added.
- Then we will perform Hyperparameter tuning, to help figure out the best hyperparameters to be used for our model.
- Next we will be using the best hyperparameters and fine-tuning our Resent50 model.
- We will also be adding in configuration for Profiling and Debugging our training mode by adding in relevant hooks in the Training and Testing( Evaluation) phases.
- Next we will be deploying our model. While deploying we will create our custom inference script. The custom inference script will be overriding a few functions that will be used by our deployed endpoint for making inferences/predictions.
- Finally we will be testing out our model with some test images of dogs, to verfiy if the model is working as per our expectations.

## Files Used

- hpo.py - This script file contains code that will be used by the hyperparameter tuning jobs to train and test/validate the models with different hyperparameters to find the best hyperparameter
- train_model.py - This script file contains the code that will be used by the training job to train and test/validate the model with the best hyperparameters that we got from hyperparameter tuning

- endpoint_inference.py - This script contains code that is used by the deployed endpoint to perform some preprocessing (transformations) , serialization- deserialization and predictions/inferences and post-processing using the saved model from the training job.
- train_and_deploy.ipynb -- This jupyter notebook contains all the code and steps that we performed in this project and their outputs.

## Hyperparameter Tuning

- The ResNet50 model with a two Fully connected Linear NN layer's is used for this image classification problem. ResNet-50 is 50 layers deep and is trained on a million images of 1000 categories from the ImageNet database. Furthermore the model has a lot of trainable parameters, which indicates a deep architecture that makes it better for image recognition
- The optimizer that we will be using for this model is AdamW ( For more info refer : https://pytorch.org/docs/stable/generated/torch.optim.AdamW.html )
- Hence, the hyperparameters selected for tuning were:
  - Learning rate - default(x) is 0.001 , so we have selected 0.01x to 100x range for the learing rate
  - eps - defaut is 1e-08 , which is acceptable in most cases so we have selected a range of 1e-09 to 1e-08
  - Weight decay - default(x) is 0.01 , so we have selected 0.1x to 10x range for the weight decay
  - Batch size -- selected only two values [ 64, 128 ]

### HyperParameter Tuning Job

### Multiple training jobs triggered by the HyperParameter Tuning Job

### Best hyperparameter Training Job

### Best hyperparameter Training Job Logs

## Debugging and Profiling
We had set the Debugger hook to record and keep track of the Loss Criterion metrics of the process in training and validation/testing phases. The Plot of the Cross entropy loss is shown below:

There is anomalous behaviour of not getting smooth output lines.

- How would I go about fixing the anomalous behaviour?
  - Making some adjustments in the pretrained model to use a different set of the fully connected layers network, ideally should help to smoothen out the graph.**
  - If I had more AWS credits, then would have changed the fc layers used in the model. Firstly would try by adding in one more fc layer on top of the existing two layers and check the results, and then if the results didn't improve much then would try by removing all the fc layers and keeping only one fc layer in the model and then rerun the tuning and training jobs and check the outputs

## Endpoint Metrics

### Results
Results look pretty good, as we had utilized the GPU while hyperparameter tuning and training of the fine-tuned ResNet50 model. We used the ml.g4dn.xlarge instance type for the runing the traiing purposes. However while deploying the model to an endpoint we used the "ml.t2.medium" instance type to save cost and resources.

## Model Deployment
- Model was deployed to a "ml.t2.medium" instance type and we used the "endpoint_inference.py" script to setup and deploy our working endpoint.
- For testing purposes , we will be using some test images that we have stored in the "testImages" folder.
- We will be reading in some test images from the folder and try to send those images as input and invoke our deployed endpoint
- We will be doing this via two approaches
  - Firstly using the Prdictor class object
  - Secondly using the boto3 client

## Deployed Active Endpoint Snapshot

## Sample output returned from endpoint Snapshot

