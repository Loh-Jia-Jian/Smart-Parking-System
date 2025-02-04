# Smart Parking System
This project is for SMJE4383 Advanced Programming Project. This web application is developed using RAG to solve real-life applications with a relatively low cost of training models.

## Start guide
### Step 1: First cd to your directory path and clone the repo to the path using:
```
git clone https://github.com/Loh-Jia-Jian/Smart-Parking-System.git
```
### Step 2: Go to the directory
```
cd Smart-Parking-System
```
### Step 3: Add the require API key on these file (system.env, firebase-config.js, firebase-adminsdk.json)
**system.env**
```
OPENAI_API_KEY = <your-api-key>
```
**firebase-config.js**
```
const firebaseConfig = {
	    apiKey: "apikey",
	    authDomain: "authdomain",
	    projectId: "project-id",
	    storageBucket: "storagebucket",
	    messagingSenderId: "sender-id",
	    appId: "app-id",
	    measurementId: "measurement-id"
  };
```
**firebase-adminsdk.json**
```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": ""
}
```
### Step 4: Create the docker image:
```
docker build -t <your-application-name> .
```

### Step 5: Run the docker on local host:
```
docker run -p 8000:8000 <your-application-name>
```
