# aws-cicd
Materials for AWS CICD workshop

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


### 1. Launch AWS CodePipeline

Click following icon to provision AWS CodePipline via AWS CloudFormation ([cf-ec2-cp.yaml](codepipelines/cf-ec2-cp.yaml)) in your AWS account.

<a href="https://console.aws.amazon.com/cloudformation/home?#/stacks/new?&templateURL=https://s3.amazonaws.com/aws-cicd-public/cf-ec2-cp.yaml" target="_blank" rel="noopener"><img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png"></a>

You can see the progress of provisioning of CodePipline on AWS CloudFormation console. After provisioning status gets to `CREATE_COMPLETED`, pls go to [CodePipline console](https://console.aws.amazon.com/codepipeline/home?region=us-east-1#/dashboard) to find your first CodePipline project.
 
Pls remember to `Confirm subscription` of two mails sent from AWS SNS topics in your mailbox, which is the email address you had written in CloudFormation.

### 2. AWS CodePipline should automatically trigger a build at first place

 