# AWS Python Web App - Deployment Commands

This file contains the main AWS CLI commands used to build, push, and deploy
the Python Flask Docker application.

## 1. Set variables

Run these commands in PowerShell and replace the placeholders with your values.

```powershell
$REGION="ap-south-1"
$ACCOUNT_ID="<ACCOUNT_ID>"
$ECR_REPOSITORY="aws-python-webapp"
$ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPOSITORY"
$CLUSTER="python-webapp-cluster"
$SERVICE="python-webapp-task-service"
$TASK_FAMILY="python-webapp-task"
```

> Do not commit AWS access keys, secret keys, passwords, `.pem` files, or other
> credentials to GitHub.

## 2. Build the Docker image

Run this from the project root, where the Dockerfile is located.

```powershell
docker build -t aws-python-webapp .
```

Check the image:

```powershell
docker images
```

## 3. Test the Docker container locally

```powershell
docker run -d -p 5000:5000 --name python-webapp aws-python-webapp
```

Check the running container:

```powershell
docker ps
```

Open:

```text
http://localhost:5000
```

Stop and remove the test container when finished:

```powershell
docker stop python-webapp
docker rm python-webapp
```

## 4. Authenticate Docker with Amazon ECR

```powershell
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"
```

## 5. Tag the Docker image

```powershell
docker tag aws-python-webapp:latest "$ECR_URI:latest"
```

Check the tag:

```powershell
docker images
```

## 6. Push the image to ECR

```powershell
docker push "$ECR_URI:latest"
```

The image should now appear in:

```text
AWS Console
→ ECR
→ Repositories
→ aws-python-webapp
```

## 7. Register the ECS task definition

Make sure `aws/task-definition.json` contains:

```text
<ACCOUNT_ID>
```

and the correct ECS execution role ARN.

Then run:

```powershell
aws ecs register-task-definition --cli-input-json file://aws/task-definition.json --region $REGION
```

Check the task definition:

```powershell
aws ecs describe-task-definition --task-definition $TASK_FAMILY --region $REGION
```

## 8. Create the ECS cluster

Skip this command if the cluster already exists.

```powershell
aws ecs create-cluster --cluster-name $CLUSTER --region $REGION
```

## 9. Create or update the ECS service

If the service already exists, update it with the latest task definition:

```powershell
aws ecs update-service `
  --cluster $CLUSTER `
  --service $SERVICE `
  --task-definition $TASK_FAMILY `
  --desired-count 1 `
  --region $REGION
```

Check the service:

```powershell
aws ecs describe-services `
  --cluster $CLUSTER `
  --services $SERVICE `
  --region $REGION
```

## 10. Force a new deployment after pushing a new image

Because the task definition uses the `latest` image tag, force ECS to launch a new task after pushing a new image:

```powershell
aws ecs update-service `
  --cluster $CLUSTER `
  --service $SERVICE `
  --force-new-deployment `
  --region $REGION
```

## 11. Check running tasks

```powershell
aws ecs list-tasks `
  --cluster $CLUSTER `
  --service-name $SERVICE `
  --region $REGION
```

Describe a task:

```powershell
aws ecs describe-tasks `
  --cluster $CLUSTER `
  --tasks <TASK_ARN> `
  --region $REGION
```

## 12. Verify the ECS service

The expected state is:

```text
Desired tasks: 1
Running tasks: 1
Pending tasks: 0
```

For an Application Load Balancer setup, also verify that the target in
`python-webapp-alb-tg` becomes healthy.

## 13. Important port configuration

The Flask application listens on:

```text
0.0.0.0:5000
```

The ECS container therefore uses:

```text
Container port: 5000
Protocol: TCP
```

When using an Application Load Balancer:

```text
Internet
   |
   | HTTP :80
   v
Application Load Balancer
   |
   | HTTP :5000
   v
Target Group
   |
   v
ECS Fargate Task
   |
   v
python-webapp container :5000
```

The ALB listener can use port 80, while the ECS container remains on port 5000.

## 14. Useful troubleshooting commands

Check ECS service events:

```powershell
aws ecs describe-services `
  --cluster $CLUSTER `
  --services $SERVICE `
  --region $REGION `
  --query "services[0].events[0:10]"
```

Check task status:

```powershell
aws ecs list-tasks `
  --cluster $CLUSTER `
  --service-name $SERVICE `
  --desired-status RUNNING `
  --region $REGION
```

Check ECR images:

```powershell
aws ecr describe-images `
  --repository-name $ECR_REPOSITORY `
  --region $REGION
```

## 15. Deployment flow

```text
Python Flask Application
        |
        v
Docker Build
        |
        v
Docker Image
        |
        v
Amazon ECR
        |
        v
ECS Task Definition
        |
        v
ECS Fargate Service
        |
        v
Fargate Task
        |
        v
python-webapp :5000
        |
        v
Application Load Balancer
```

## Notes

- Region used by this project: `ap-south-1` (Mumbai).
- ECR repository: `aws-python-webapp`.
- ECS cluster: `python-webapp-cluster`.
- Task definition family: `python-webapp-task`.
- Container name: `python-webapp`.
- Container port: `5000`.
- Fargate CPU: `0.5 vCPU` (`512` CPU units).
- Fargate memory: `1 GB` (`1024` MiB).
