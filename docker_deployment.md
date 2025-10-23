# Docker Deployment WSL2 Tutorial

## Requirements
- Windows 10 version: 10.0.19045 Build 19045
- CPU Virtualization (BIOS)

## Docker Installation
1. Follow the steps in the link below to install Docker Desktop for Windows 10.

https://docs.docker.com/desktop/setup/install/windows-install/

### Docker Configuration
1. Open docker desktop and navigate to Settings-->Resources-->WSL Integration.

2. Enable Integration with my Default WSL Distro

3. Enable Ubuntu

## Deployment

1. Navigate to an empty directory and clone the application repository
`git clone https://github.com/navidr08-hub/microblog.git`

2. Create the Docker Network
`docker network create microblog-network`

3. Run the mysql container (Fill the blanks)
`docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=microblog -e MYSQL_USER=microblog -e MYSQL_PASSWORD=<db-password> --network microblog-network     mysql:latest`

4. Run the elasticsearch container
`docker run --name elasticsearch -d --rm -p 9200:9200 -e discovery.type=single-node -e xpack.security.enabled=false --network microblog-network -t docker.elastic.co/elasticsearch/elasticsearch:9.0.3`

5. Run the redis server container
`docker run --name redis -d -p 6379:6379 --network microblog-network redis:latest`

5. Run the microblog app container (Fill the blanks)
`docker run --name microblog -d -p 8000:5000 --rm -e SECRET_KEY=<secret-key> -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true -e MAIL_USERNAME=<your-mail-username> -e MAIL_PASSWORD=<app-password> --network microblog-network -e DATABASE_URL=mysql+pymysql://microblog:<db-password>@mysql/microblog -e ELASTICSEARCH_URL=http://elasticsearch:9200 -e MS_TRANSLATOR_KEY=<ms_translator_key> -e MS_TRANSLATOR_REGION=<ms_translator_region> -e REDIS_URL=redis://redis:6379/0 microblog:latest`

6. Run the RQ worker container (Fill in the blanks)
`docker run --name rq-worker -d --rm -e SECRET_KEY=<secret-key> -e MAIL_SERVER=smtp.googlemail.com -e MAIL_PORT=587 -e MAIL_USE_TLS=true -e MAIL_USERNAME=<you-mail-username> -e MAIL_PASSWORD=<mail-password> --network microblog-network -e DATABASE_URL=mysql+pymysql://microblog:<db-password>@mysql/microblog -e REDIS_URL=redis://redis:6379/0 --entrypoint venv/bin/rq microblog:latest worker -u redis://redis:6379/0 microblog-tasks`

6. Check the docker logs to see if any errors occured
`docker logs microblog`

## Test Application
All deployment steps are complete, all thats left is to test the application, to verify functionality.

1. Test Authentication
- User Registration
 - Create basic user in regular use case ... Done
 - Enter problematic text in fields ... 

- User login ... Done

- Password Reset ... Done

2. Test Posts and Profile
- Post something ... Done
- Translate a post ... Done
- Change about me in Profile ... Done
- Change username ... Done

3. Test Explore ... Done