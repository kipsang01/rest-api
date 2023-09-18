# SIMPLE DJANGO REST FRAMEWORK APP
simple DRF app to display development process and deployment automation of a large application.
## USAGE
#### Authorization
Uses OIDC built on top of OAuth2.0.  
All OAuth2.0 url paths apply with prefix `/o/`, check the documentation [here](https://django-oauth-toolkit.readthedocs.io/en/2.3.0/oidc.html)  

Get token endpoint
- url: ``localhost:8000/o/token``
  - POST :
    - params: ``username, password``
    - returns: ``access_token, refresh_token,``
####  Customers
Customers endpoint. Accepts ``GET, POST, PUT, DELETE``  
Authorization: ```Bearer <token>```
  - GET:
    - list-url: ``localhost:8000/api/customers/``
    - specific-url: ``localhost:8000/api/customers/<customer_id>/``
    - response: ``status_code: 200 ``  


  - POST:
    - url: ``localhost:8000/api/customers/`` 
    - params: 
      - ``name``: optional
      - ``code``: required
      - ``phone_number``: required
    - response: ``status_code: 201 `` 


  - DELETE:
    - url: ``localhost:8000/api/customers/<customer_id>/``
    - params: ``none``
    - response: ``status_code: 204``
  
####  Orders
Customers endpoint. Accepts ``GET, POST, PUT, DELETE``  
Authorization: ```Bearer <token>```
  - GET:
    - list-url: ``localhost:8000/api/orders/``
    - specific-url: ``localhost:8000/api/customers/<order_id>/``
    - response: ``status_code: 200 ``  


  - POST:
    - url: ``localhost:8000/api/orders/`` 
    - params: 
      - ``customer``: int,  required
      - ``item``: string, required
      - ``amount``: float, required
    - response: ``status_code: 200 ``

  - DELETE:
    - url: ``localhost:8000/api/orders/<order_id>/``
    - params: ``none``
    - response: ``status_code: 204``
  

## DEVELOPMENT
To run in development environment:
- Clone the project
- create ``.env`` file with the following variables:
  - DATABASE_NAME
  - DATABASE_USER
  - DATABASE_PASSWORD
  - DATABASE_HOST
  - DATABASE_PORT
  - AFRICASTALKING_API_KEY
  - AFRICASTALKING_USERNAME
  - AFRICASTALKING_SENDER_ID
  - DEBUG_MODE
  - DJANGO_ALLOWED_HOSTS
  - DJANGO_SECRET_KEY
  - OIDC_RSA_PRIVATE_KEY
  - >To get `AFRICASTALKING` credentials visit [africastalking](https://developers.africastalking.com/).

- create postgres database.
- pip install requirements:
  - ``pip install -r requirements.txt``
- run migration commands:
  - ``python manage.py makemigrations``
  - ``python manage.py migrate``
- to create superuser:
  - ``python manage.py createsuperuser --username=<username> --email=<email> --password=<password>``
- run django server:
  - ``python manage.py runserver``
- to run tests:
  - ``pytest --junitxml=pytest.xml  --cov-report=term-missing:skip-covered --cov=api */tests/*``
    
### Integration and Deployment
This application is configured to use github actions for continuous integration and deployed to AWS cloud using Terraform  

> Uncomment github-actions workflow jobs to create AWS infrastructure and build, push and update the containers
  

Add the following to repository secrets:  
- DATABASE_NAME
- DATABASE_USER
- DATABASE_PASSWORD
- DATABASE_HOST
- DATABASE_PORT
- AFRICASTALKING_API_KEY
- AFRICASTALKING_USERNAME
- AFRICASTALKING_SENDER_ID
- DJANGO_SECRET_KEY
- OIDC_RSA_PRIVATE_KEY

And this to repository variables:
- DEBUG_MODE
- DJANGO_ALLOWED_HOSTS

Setting up AWS infrastructure requires github actions to access the cloud:
- using open ID Connect: Follow this guide [https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/](https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/).
- or using access keys and secret keys with roles.

The infrastructure uses AWS Elastic Container Services(ECS) to run the images stored in Elastic Container Registry (ECR).  
Terraform uses S3 to store state files
> Some of the resources created by this deployment automation are not free. Remember to destroy them when you don't need them.
  
##### running commands in running  container:
- Install AWS ECS CLI. Follow this [guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI.html).
- Ensure ECS Exec is enabled on task definitions.
- Add Container Task IAM role has SSM permissions.
- IAM role used in CLI should also have permissions to Execute Command in ECS
- Enable ECS Exec:
  - ``aws ecs update-service \
    --cluster <cluster-name> \
    --task-definition <task-definition-name> \
    --service <service-name> \
    --enable-execute-command \``
- Login to container:
- ``aws ecs execute-command --cluster <cluster-name> \
    --task <task-id> \
    --container <container-name> \
    --interactive \
    --command "/bin/sh"``  
- Then you can run commands like migrations:
  - ``python manage.py run migrations``






