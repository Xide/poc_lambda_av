
# Prerequisites

- Docker
- Docker-compose
- [mc](https://docs.min.io/docs/minio-client-complete-guide.html)

# Setup

```sh
docker-compose up --build

# In another terminal, after boot
mc alias set s3 http://localhost:9000 minio minio123
mc mb s3/staging
mc mb s3/accepted
mc mb s3/rejected
mc event add s3/staging arn:minio:sqs::TEST:amqp --event put
```

# Usage

## Sane file
```sh
mc cp ./Dockerfile s3/staging

# Check that the file is accepted
mc ls s3/accepted
```

## EICAR test file
```sh
curl -o eicar.com.txt https://secure.eicar.org/eicar.com.txt
mc cp ./eicar.com.txt s3/staging

# Check that the file is rejected
mc ls s3/rejected
```

## Monitoring

MinIO admin : `http://localhost:9001` (`minio`:`minio123`)
RabbitMQ    : `http://localhost:15672` (`myuser`:`mypassword`)


# TODO

- clamd supervisor (s6?)
- clamd signature database updates
- variables
  - minio
  - rabbitmq
- manual message acknowledge
- alerts to external system
