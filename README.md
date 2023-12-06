# Response System to City Disaster - RSCD
Advanced Software Engineering - Group10  

This is the repository for the ASE project of Group 10.  

You can visit the live demo here: 
## Production Build
[https://rscd.iocky.com](https://rscd.iocky.com)  
[https://mine.bf](https://mine.bf)   
(mine.bf link may only be available for a limited time.)  
## Staging Build with Staging APIs
[https://rscdstaging.iocky.com/](https://rscdstaging.iocky.com/)

# Group Members  
To contact all group members, please send an email to: [group10@iocky.com](mailto:group10@iocky.com)

KAIYU CHEN - chenka@tcd.ie  
DEHAO DONG - ddong@tcd.ie  
JIAWEI SHEN - shenj3@tcd.ie  
PEICHEN SUN - sunpe@tcd.ie  
HAOKUN ZHANG - zhangh9@tcd.ie  
XIAOYAO ZHU - zhux7@tcd.ie  
YIFAN ZHU - zhuyi@tcd.ie  

# Project Description  
This system involves citizens of Dublin City reporting a disaster at any location in the city. By reporting the disaster to the Emergency Response Team, the Emergency Response Team can then take corresponding measures to address the disaster in a timely manner.  

# Project Structure  
The project is divided into two parts: the front-end and the back-end. The front-end is developed using React, and the back-end is developed using Django. The front-end and back-end are connected through RESTful APIs.  

# How to run the project  
## Back-end
### Install the required packages
Install the required packages in the virtual environment
```shell
pip install -r requirements.txt
```
### Go to the project directory
```shell
cd backend
```

### Create a ```.env``` file
```shell
touch .env
```

### Add the following content to the ```.env``` file
```shell
DJANGO_SECRET_KEY=
DJANGO_DEBUG=
DJANGO_DB_NAME=
DJANGO_DB_USER=
DJANGO_DB_PASSWORD=
DJANGO_DB_HOST=
DJANGO_DB_PORT=
```

### Run the following commands
```shell
python manage.py makemigrations
```

```shell
python manage.py migrate
```

### Run the server
```shell
python manage.py runserver
```

## Front-end

### Before Running

Add your Google Map API and backend url to ```.env``` file

```shell
VUE_APP_GOOGLE_MAP_API=
VUE_APP_BACKEND_URL=http://[your_backend_host]:[your_backend_port]/dr/api
```

### Build Setup

#### install dependencies

```
npm install
```

#### serve with hot reload at localhost:8080

```
npm run dev
```

#### build for production with minification

```
npm run build
```

#### lint

```
npm run lint
```
