## aws-lambda-sls

Python Simple Serverless for AWS Lambda Project.

## Quick Start
You can create lambda Lambda sls service:

```
from aws_lambda_sls import LambdaSls

app = LambdaSls("sls_app")
app.run()
```

## Register Lambda Function
```
from aws_lambda_sls import register_function


@register_function
def lambda_handler(event, context):
    return {
        "event": event,
        "aws_request_id": context.aws_request_id
    }
```

## Commands
Create App
```
Usage: sls create-app [OPTIONS] PROJECT_NAME

Options:
  --help  Show this message and exit.
```

Package App
```
Usage: sls package [OPTIONS]

Options:
  --generate-sam    Create a single packaged file. By default, the 'out'
                    argument specifies a directory in which the package assets
                    will be placed.  If this argument is specified, a single
                    zip file will be created instead.
  --stage TEXT      lambda function stage, default dev.
  --out TEXT        lambda package out directory, default dist.
  --force-download  If force download dependency lib, default false.
  --help            Show this message and exit.
```

Deploy App
```
Usage: sls deploy [OPTIONS]

Options:
  --stage TEXT        Name of the sls stage to deploy to. Specifying a new sls
                      stage will create an entirely new set of AWS resources.
  --profile TEXT      Override profile at deploy time.
  --deploy-file TEXT  deployment file.
  --s3-key TEXT       s3 file.
  --help              Show this message and exit.
```

Create Local Lambda Server.
```
Usage: sls local [OPTIONS]

Options:
  --host TEXT
  --port INTEGER
  --stage TEXT        Name of the sls stage for the local server to use.
  --deploy-file TEXT  deployment file.
  --log-file TEXT     output log file path.
  --help              Show this message and exit.
```
