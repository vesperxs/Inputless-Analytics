![myotis-logo](/images/logo-black-no-sfondo.png)

# Data Exploration *PIPELINE* for Legal NLP!

- Empowered AI SAAS for Legal NLP.
- Quickly upload, analyze and interact with data.
- Extraction parsing and processing informations/attributes from text.
- It has important applications in networking, software engineering, and in visual interfaces for other technical domains.
- Multi Tenant / Multi Account.
- Two Factor Authentication
- Administration Dashboard
- Indexing and Searching Documents
- Document Parser / Analyzer: doc, docx, pdf, exel , txt, ecc.
- System Chat Communicator
- Javascript Code Obfuscator.
- Fully reprogrammable.



# Introduction:

Inputless Myotis is a data exploration tool that make easier to navigate through italian LEGAL information documents extracted from raw text!

This project has been deployed by Giovanni Errico - Leonardo Trisolini since 2020 to 2022 and we wish it will be continued by the community.





# Features / sssshots :)

###  Main Screen

![main screen](/images/main_screen.png)

![account registrations](/images/registration_process1.png)

### Dashboard

![](/images/dashboard.png)

### Upload - Graph Creator - Content Store

![](/images/upload.png)

#### Dynamic graph visualizer layouts

![Inteface](/images/graph.png)

### Circular Layout

![](/images/graph2.png)



#### Dagre Layout

![dagre](/images/dagre.png)



#### Sparse Layout



![](/images/sparse.png)



#### System Chat Communicator

![](/images/chat2.png)



![](/images/chat1.png)



#### Table View 

- Extract

- Print

- Organize reprogrammable

- Download 

  

![](/images/table.png)



# Notes:

No AI model is included in this software ! 

It was originally build to support Italian Legal System so feel free to customize and adapt tags / annotations to your needs.

At the end you have something to enjoy as i already did !



# Requirements:

- Docker
- Docker compose
- Doccano Annotator
- Spacy NLP



# The Pipeline includes:

-  Grafana (analytics web application)
- Nginx ( reverse proxy )
- Celery ( task worker )
- Redis ( in-memory database )
- Postgres ( RDBMS database )
- Postgres - Exporter ( metrics )
- PG Backups ( postgress backup )
- Prometheus ( metrics )
- Clamav (antivirus)



# Deploy:

- ## Build:   

  ## `docker-compose --compatibility up --build `

- ## Staging:  

  ## `docker-compose -f docker-compose.staging.yml --compatibility up --build`

- ## Production: 

  ##  `docker-compose -f docker-compose.prod.yml --compatibility up --build`

- ## Stop:

  ##  `docker-compose --compatibility down -v `

- ## Clear images and containers:

  ## `docker system prune -af`



# Deploy postgress ssl certificates:



- ## *Certification authority*:   

  

  ```
  Generate RootCA.pem, RootCA.key & RootCA.crt:
  
  openssl req -x509 -nodes -new -sha256 -days 1024 -newkey rsa:2048 -keyout RootCA.key -out RootCA.pem -subj "/C=US/CN=Example-Root-CA"
  openssl x509 -outform pem -in RootCA.pem -out RootCA.crt
  ```

  

- ## Domain name certificate: 

  ```
  First, create a file `domains.ext` that lists all your local domains
  
  authorityKeyIdentifier=keyid,issuer
  basicConstraints=CA:FALSE
  keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
  subjectAltName = @alt_names
  [alt_names]
  DNS.1 = localhost
  DNS.2 = fake1.local
  DNS.3 = fake2.local
  
  
  ```
  
  ```
  Generate localhost.key, localhost.csr, and localhost.crt:
  
  openssl req -new -nodes -newkey rsa:2048 -keyout localhost.key -out localhost.csr -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=localhost.local"
  openssl x509 -req -sha256 -days 1024 -in localhost.csr -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out localhost.crt
  ```
  
  

# Django schema migrations after build:

- ` docker exec -it Web bash`

- ./manage.py makemigrations

- ./manage.py migrate

  

# Suggestions:

### Please Note:

- This project is under  constant developement .. Fill free to contribute to it!

- To fully deploy the production enviroment you need the server supports *HTTPS* with nginx-proxy-letsencrypt,  so in this env you'll uncomment tags in  `docker-compose.prod.yml` ,than rename the nginx-production folder to nginx or make it point directly in the following configuration.

- In the enviroment production please modify access permissions to the following folder:

  `chown -r user:user docker-data/appdata` 





```dockerfile
# nginx-proxy:
  #   container_name: nginx-proxy
  #   build: nginx
  #   restart: always
  #   ports:
  #     - 443:443
  #     - 80:80
  #   volumes:
  #     - certs:/etc/nginx/certs
  #     - html:/usr/share/nginx/html
  #     - vhost:/etc/nginx/vhost.d
  #     - /var/run/docker.sock:/tmp/docker.sock:ro
  #     - ./logs:/var/log/nginx
  #     - static_volume:/app/staticfiles
  #   depends_on:
  #     - web
  #   networks:
  #     - main

  # nginx-proxy-letsencrypt:
  #   image: jrcs/letsencrypt-nginx-proxy-companion
  #   env_file:
  #     - ./.env.prod.proxy-companion
  #   volumes:
  #     - /var/run/docker.sock:/var/run/docker.sock:ro
  #     - certs:/etc/nginx/certs
  #     - html:/usr/share/nginx/html
  #     - vhost:/etc/nginx/vhost.d
  #     - acme:/etc/acme.sh
  #   depends_on:
  #     - nginx-proxy
  #   networks:
  #     - main

```







# TODO:

- [ ] Unit Test

- [ ] Integration Test

- [ ] Smoke Test

- [ ] Add Terraform script 

- [ ] Add pipeline CI/CD ( JENKINS )





# Known Errors:













