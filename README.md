# Finxi task

An application to make droid parts demands and finalize them, using Python + Django Rest Framework and Docker container.


## Building and running

Using Docker Compose, just run the following command to build, run tests and run the application server from the root directory.

```bash
sudo docker-compose up
```

## API requests
After starting the server, import the list of requests [file](./postman_requests.json) to Postman or Insomnia to test and verify the API working properly. Some of the calls you can make are:
- API GET /users/
- API GET /user/{id}
- API DELETE /user/{id}
- API GET /groups/
- API GET /group/{id}
- API GET /demands/
- API POST /demands/
- API GET /demand/{id}
- API PUT /demand/{id}/finalize