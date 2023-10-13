# jowl

<summary>This is a flask web application to help people in e-comm to bulk sending emails.</summary>
This application will be in docker.

----------------
### To Build The application Via Docker

```
docker build -t mailer .
```

### To Run The Application
```
docker run -p 5000:5000 mailer
```
----------------
### To Run The Application in the background
```
docker run -d -p 5000:5000 mailer
```
----------------
### One Command : To Build && Run The application Via Docker-Compose
```
docker-compose up
```
----------------
### If you don't have docker installed
Refer to the
[Docker Web Site](https://www.docker.com/products/docker-desktop/)

----------------
### API Documentation
After successfully downloading the project and running it, here's the API that you can use

__Base URL__ : http://localhost:5000


__Reasoning's APIS__
| Method Type | API  | Description |
| -------- | -------- | -------- |
| _GET_ | / | Default Route |
| _GET_ | /filter | route to filter mails |
| _GET_ | /send_email | route to bulk sending emails |

----------------