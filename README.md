# GraphRAG application 


# Setup 
The application has been developed using python3.9.0. To get started, we will be using the neo4j locally and openai to develop the the application. To get started, we have to 

1. Create a .env file and save the openai key. 
2. Install docker and docker-compose and run  ``` docker-compose up -d ```
to run the neo4j server. We also enable modules to be used in the file so that we can run the openai services and create vectorised database.
3. Create python environment to get started using ``` pyenv virualenv 3.9.0 graph@3.9.0 ``` and activate it using ``` pyenv activate graph@3.9.0 ```
4. Install the python requirements ``` pip install -r requirements.txt ```
5. Run the application using ``` python -u main.py ```
