# aws-cicd
Materials for AWS CICD workshop

# Content
* [Prerequisites](#prerequisites)
* [Hands-on](hands-on)
  * [CI/CD with EC2 on AWS](#cicd-with-ec2-on-aws)
    * [1. Launch AWS CodePipeline](#1-launch-aws-codepipeline)
    * [2. AWS CodePipline should automatically trigger a build at first place](#2-aws-codepipline-should-automatically-trigger-a-build-at-first-place)
    * [3. Take a look at every component in the overall CodePipeline](#3-take-a-look-at-every-component-in-the-overall-codepipeline)
    * [4. Take a look at our RESTful API service](#4-take-a-look-at-our-restful-api-service)
    * [5. Delete hands-on resources](#5-delete-hands-on-resources)

# Prerequisites

1. An AWS ([Amazon Web Service](https://aws.amazon.com/)) account W/ **administrator permission**, if you have none, to get one !

There are few things need your notices and actions in your AWS account
  * All the hands-on activities will be in region **us-east-1**, codes are not tested in other regions.
  * And you need to make sure you can create bucket and put files on [S3](https://s3.console.aws.amazon.com/s3/home?region=us-east-1)... due to you can not use it before account activated successfully.
  * [Create a SSH key](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair) (e.g. cicd) in us-east-1 region under your AWS account.
  
2. The AWS expenses will occur in the hands-ons, it should cost less than USD $1.0 for each hands-on...
3. A public [GitHub](https://github.com/) account, if you have none, to get one !

There are two more things need your actions in your GitHub account
  * Fork this repo to under your GitHub account
  * Create a [valid OAuth token from GitHub](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/), we will use it in AWS Pipeline service. 


# Hands-on

I am trying to leverage as most managed services on AWS as we can, so I picked S3, [CodePipline](https://aws.amazon.com/codepipeline/), CodeBuild and CloudFormation as a foundation for our hands-on.    

Frankly to say, there are variety of technology combinations doing CI/CD on every environment (In this case, is AWS), so my choices here may not be the most suitable for your needs, it simply plays as a quick start to bring you the overall concepts and a PoC to home. And I hope, it can help you an idea to tailor your own one. 

## CI/CD with EC2 on AWS
[Back to top](#content)


### 1. Launch AWS CodePipeline
[Back to top](#content)

Click following icon to provision AWS CodePipline via AWS CloudFormation ([cf-ec2-cp.yaml](codepipelines/cf-ec2-cp.yaml)) in your AWS account.

<a href="https://console.aws.amazon.com/cloudformation/home?#/stacks/new?&templateURL=https://s3.amazonaws.com/aws-cicd-public/cf-ec2-cp.yaml" target="_blank" rel="noopener"><img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"></a>

1. Fill up the parameters whom are empty
2. Click next and next again
3. Check all confirmation questions for access IAM resources
4. Click create ChangeSet button
5. Click execute and will bring you to [CloudFormation console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1) automatically.
 

You can see the progress of provisioning of CodePipline on AWS CloudFormation console. After provisioning status gets to `CREATE_COMPLETED`, pls go to [CodePipline console](https://console.aws.amazon.com/codepipeline/home?region=us-east-1#/dashboard) to find your first CodePipline project.
 
Pls remember to `Confirm subscription` of two mails sent from AWS SNS topics in your mailbox, which is the email address you had written in CloudFormation.

### 2. AWS CodePipline should automatically trigger a build at first place
[Back to top](#content)

You can see the CodePipline project starts to trigger a build automatically in few minutes. Due to we set `PollForSourceChanges: True` in Source action.


After the service provisioning gets to `CREATE_COMPLETED`, you can get the endpoint FQDN at the row ALBDNSName in Output tab in AWS CloudFormation console. let's veirfy your build whether successfully !

```bash
curl http://<ALBDNSName>
Welcome to my home
```

The very simple API impl. is [api/main.py](api/main.py) you can take a look if interested in.

### 3. Take a look at every component in the overall CodePipeline
[Back to top](#content)

Take a look on [CodePipline console](https://console.aws.amazon.com/codepipeline/home?region=us-east-1#/dashboard) and corresponding docs as follows to clarify our questions.

#### 3.1 What is Stage, action and transition ?

* http://docs.aws.amazon.com/codepipeline/latest/userguide/concepts.html#concepts-how-it-works

#### 3.2 What types of actions ?

* http://docs.aws.amazon.com/codepipeline/latest/userguide/integrations-action-type.html

The action types we are using are...

Category | Action
---------|--------
Source | GitHub
Build | AWS CodeBuild
Deploy | CloudFormation
Approval | Manual approval

You can see more details in [cf-ec2-cp.yaml](codepipelines/cf-ec2-cp.yaml) 

#### 3.3 Why not use Jenkins, CodeDeploy, or a or b or c ?

Let's say it again, this hands-on simply plays as a quick start to bring you the overall concepts and a PoC to home. And I hope, it can help you an idea to tailor your own one.

But I still can say that, CodePipeline using Jenkins need to launch a long running EC2 instance behind the scene, it is too costly for a PoC. And CodeDeploy can support variety of deployment methods (Lambda, ECS, etc), but in the end, I still need to use CloudFormation to provision monitoring related resources based on end-to-end point of view. And also, CloudFormation is more portable running in diffrent CI servers (Maybe :P).


### 4. Take a look at our RESTful API service
[Back to top](#content)

The very simple API impl. is [api/main.py](api/main.py) you can take a look if interested in.

#### 4.1 healthcheck API

```bash
curl http://<ALBDNSName>/healthcheck
Hello World!
```

This API is used by ALB and auto-scaling group, auto-scaling group will increase/decrease based on the responses of this API on every EC2 instance.

The configuration order will be ALB -> Target group -> Auto-scaling group -> Auto-scaling group configuration -> EC2. You can get start on following doc.

* http://docs.aws.amazon.com/autoscaling/latest/userguide/autoscaling-load-balancer.html


#### 4.2 What will happen if we want to update/deploy our new codes to existing service ?

In this hands-on we are using A/B deployment (create 2 new EC2s -> all healthchek passed -> delete 2 old EC2s), the details in following doc

* http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatepolicy.html

Take a look on [cf-ec2.yaml](cd/cf-ec2.yaml) for more details.

#### 4.3 To use `AWS::CloudFormation::Init` instead of OpsWorks service

OpsWorks service has a lot of pitfalls and performance issues according my experiences, I recommend to use `AWS::CloudFormation::Init` instead.

* http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-init.html

Actually, `AWS::CloudFormation::Init` is based on [cloud-init](https://cloudinit.readthedocs.io/en/latest/) project.


#### 4.4 sleep API

```bash
curl http://<ALBDNSName>:8080/sleep/30
sleep for 30 secs
```

This API is used to create a response latency (by seconds) of our service, to trigger the backend alarm.

See the service alarm on [CloudWatch Alarm console](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#alarm:alarmFilter=inOk)

See the service dashboard on [CloudWatch Dashboard](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:)

All these basic stuffs can be created by AWS CloudFormation

* http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
* http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dashboard.html

But actually, there are still more complicated usecases the CloudFormation can not fulfill them in a out-of-box manner, in these cases, we can consider to use `AWS::CloudFormation::CustomResource` to deal them. 

* http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html

`AWS::CloudFormation::CustomResource` is actually a Lambda function extension plugged in CloudFormation service.

#### 4.5 secret API

TBD...



### 5. Delete hands-on resources
[Back to top](#content)

1. Approve `ApproveForDeletion` action in CodePipeline

Approve this action will keep to delete CloudFormation stacks `*-ec2` and `*-ec2-vpc`
 
2. Delete S3 bucket for CodePipeline artifacts

Go to [S3 console](https://s3.console.aws.amazon.com/s3/home?region=us-east-1) and rm bucket: `*-cicd-test`

3. Delete CodePipeline CloudFormation stack
Go to [CloudFormation console](https://console.aws.amazon.com/cloudformation/home?region=us-east-1) and delete CodePipline stack (The stack name was given by you at start).

