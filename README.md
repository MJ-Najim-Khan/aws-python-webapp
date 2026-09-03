\# AWS Python Web Application



A containerized Python Flask web application deployed on AWS using Docker, Amazon ECR, Amazon ECS Fargate, and an Application Load Balancer.



\## Architecture



The application uses the following AWS services:



\- Amazon ECR

\- Amazon ECS

\- AWS Fargate

\- Application Load Balancer

\- AWS Lambda

\- Amazon API Gateway

\- IAM

\- Amazon CloudWatch



\## Architecture Flow



Internet

&#x20;   |

&#x20;   v

Application Load Balancer

&#x20;   |

&#x20;   v

Amazon ECS Fargate

&#x20;   |

&#x20;   v

Docker Container

&#x20;   |

&#x20;   v

Flask Application



Serverless API:



API Gateway

&#x20;   |

&#x20;   v

AWS Lambda

&#x20;   |

&#x20;   v

JSON Response



\## Technologies



\- Python

\- Flask

\- Docker

\- AWS ECS Fargate

\- Amazon ECR

\- Application Load Balancer

\- AWS Lambda

\- API Gateway

\- IAM

\- CloudWatch



\## Application Endpoints



\### Home



GET /



Returns the Flask web application homepage.



\### Hello API



GET /hello



Example response:



{

&#x20;   "message": "Hello from ECS Fargate!",

&#x20;   "application": "Python Web App",

&#x20;   "status": "success"

}



\## Docker



Build the Docker image:



docker build -t aws-python-webapp .



Run the container:



docker run -p 5000:5000 aws-python-webapp



\## AWS Deployment



The Docker image is stored in Amazon ECR and deployed using Amazon ECS Fargate.



Deployment flow:



Docker

&#x20; |

&#x20; v

Amazon ECR

&#x20; |

&#x20; v

ECS Fargate

&#x20; |

&#x20; v

Application Load Balancer

&#x20; |

&#x20; v

Internet



\## Lambda API



AWS Lambda is integrated with API Gateway to provide a serverless API endpoint.



\## Security



AWS IAM roles are used to control access between AWS services.



Secrets, credentials, private keys, and environment files are excluded from the repository.



\## Future Improvements



\- CI/CD using GitHub Actions

\- HTTPS using AWS Certificate Manager

\- Custom domain using Route 53

\- Auto Scaling

\- Amazon RDS integration

\- CloudWatch monitoring

\- Infrastructure as Code using AWS CloudFormation or Terraform



\## Author



MOHAMED NAJIM KHAN MJ

