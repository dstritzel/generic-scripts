# generic-scripts

A collection of utility scripts for various DevOps and automation tasks.

## Table of Contents

- [AWS Scripts](#aws-scripts)
  - [Load Balancer Information Puller](#load-balancer-information-puller)
- [Usage](#usage)
- [Prerequisites](#prerequisites)

## AWS Scripts

### Load Balancer Information Puller

**Location:** `aws/pull-lb-info/list-lb-info.py`

**Description:** 
This script retrieves detailed information about all Elastic Load Balancers (ELBv2) in your AWS account and outputs the data in JSON format.

**Features:**
- Lists all Application Load Balancers (ALB) and Network Load Balancers (NLB) in your account
- Retrieves associated listeners for each load balancer
- Outputs comprehensive load balancer configuration in JSON format
- Includes load balancer attributes like ARN, DNS name, scheme, state, type, VPC ID, and availability zones

**Usage:**
```bash
cd aws/pull-lb-info
pip install -r requirements.txt
python list-lb-info.py
```

**Output:**
The script outputs a JSON array containing detailed information about each load balancer, including:
- Load balancer metadata (name, ARN, DNS name, etc.)
- Configuration details (scheme, state, type)
- Network information (VPC ID, availability zones, security groups)
- Associated listeners with their configurations

**Prerequisites:**
- AWS CLI configured with appropriate credentials
- IAM permissions for `elasticloadbalancing:DescribeLoadBalancers` and `elasticloadbalancing:DescribeListeners`
- Python 3.x
- boto3 library (see requirements.txt)

## Usage

Each script directory contains its own `requirements.txt` file. Install dependencies before running:

```bash
cd <script-directory>
pip install -r requirements.txt
python <script-name>.py
```

## Prerequisites

- Python 3.x
- AWS CLI configured (for AWS scripts)
- Appropriate IAM permissions for the resources you're accessing
