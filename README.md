# Sandman
[![Build Status](https://travis-ci.org/porthunt/sandman-aws.svg?branch=master)](https://travis-ci.org/porthunt/sandman-aws)

Sandman was designed to reduce the costs of your AWS EC2 instances. Using Sandman, you can configure which and when to stop them. You simply need to deploy Sandman's lambda functions and that's it, it will take care of the rest.

## Customizing
Before deploying, you can customize where to deploy the lambda functions and at which time you want to start/stop the instances. Open the file `variables.tf` and modify the default values. You can modify:
* The AWS region you want to deploy Sandman to.
* The start and stop schedules (aka when Sandman will start and stop your instances).
* The python runtime (Sandman is compatible with Python >3.6).

### Ignore instances
Sometimes you have instances that need to run 24/7. Sandman can **ignore** instances with the tag `sandman=ignore`. So if you have an instance that you don't want Sandman to touch, just **add this tag to your EC2 instance**.

## How to deploy
To deploy Sandman on your account, you simply need to run `./deploy.sh`. This script will create:
* The policy that allows the lambda function to `StartInstances`, `StopInstances` and `DescribeInstances`.
* The role that uses the previous policy.
* The lambda functions to start and stop the instances.
* Cloudwatch events that triggers the lambda functions.

```shell
$ git clone https://github.com/porthunt/sandman-aws.git
$ cd sandman-aws
$ vim variables.tf  # modify the variables
$ ./deploy.sh
```
  
## Removing Sandman
In case you don't want to have Sandman anymore, just run `./destroy.sh`.

## License
Sandman is completely unlicensed. Feel free to just modify it as you want.
