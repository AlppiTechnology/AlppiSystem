
### Install Docker
~~~ sh
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user
docker ps
~~~


### Install Docker-Compose
~~~ sh
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s | tr '[:upper:]' '[:lower:]')-$(uname -m) -o /usr/bin/docker-compose && sudo chmod 755 /usr/bin/docker-compose && docker-compose -version. 
~~~

###
~~~ sh
# Create app file
mkdir /app/
cd /app/

# clone repos
git clone https://patrickpiccini:<key>@github.com/AlppiTechnology/AlppiAuthentication.git

git clone https://patrickpiccini:<key>@github.com/AlppiTechnology/AlppiSystem.git

git clone https://patrickpiccini:<key>@github.com/AlppiTechnology/PopulateDB.git

# build images of Auth and Sys
mv deployments/Dockerfile .
mv deployments/docker-compose.yml .
# Auth
docker build -t alppiauthentication:v1.0.0 .
# sys
docker build -t alppisystem:v1.0.0 .

docker-compose up -d
~~~