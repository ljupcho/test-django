# todo app with docker
<br/>
First you would create a dir for this project and in it:</br>
1). clone the repo https://github.com/ljupcho/docker-nginx-python2-db-redis<br/>
2). clone the project https://github.com/ljupcho/todo<br/>
3). <b>cd docker-nginx-python2-db-redis</b> && <b>./scripts/startup.sh</b><br/>
This should create all the docker containers and set up everything, including insallation of the packages in requirements.txt files for both the web and consumers. they are set up with uwsgi with nginx proxy. using redis to store jobs/tasks for a the celery queue. docker-compose.yml file is the main file for building the docker services/containers.
<br/><br/>
The consumers are kept alive using supervisor that runs the celery worker commands.
Upon creating a task from the app a job/task is being dispached in redis and a consumer picks it up through the celery queue system. if change is made only restarting the consumer's docker container is enough with: <b>docker-compose restart consumers</b>
<br/><br/>
You would access the app in browser with <b>http://localhost:8081/todolist/</b> and ports are exposed to:<br/>
 mysql docker - 3306<br/>
 web/consumer uwsgi containers - 9000<br/>
 redis - 6379<br/>
 Make sure those are not taken as well. In the docker app there is .env file if you prefer to adjust the ports, version of some packages or database credentials.
<br /><br />
Check the consumers running:<br />
<b>docker-compose exec consumers bash</b><br />
<b>ps aux | grep worker</b><br />
<br /><br />
