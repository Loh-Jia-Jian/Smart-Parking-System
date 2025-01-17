# Smart Parking System
This project is for SMJE4383 Advanced Programming Project. This web application is developed using RAG to solve real-life applications with a relatively low cost of training models.

## Start guide
First cd to your directory path and clone the repo to the path using:
```
git clone https://github.com/Loh-Jia-Jian/Smart-Parking-System.git
```

Create the docker image:
```
docker build -t <your-application-name> .
```

Run the docker on local host:
```
docker run -p 8000:8000 <your-application-name>
```

### For developer
Command to run the system on terminal
```
uvicorn app.main:app --reload
```