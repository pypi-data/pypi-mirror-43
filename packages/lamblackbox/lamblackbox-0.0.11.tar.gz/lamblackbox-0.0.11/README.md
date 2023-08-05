# Lamblackbox

This is a AWS Lambda function logging library.

## Install

```
pip install lamblackbox
```

## Usage

### API Gateway

Code.

```
import lamblackbox
import json


@lamblackbox.apigateway
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }
```

Logged.

```
START RequestId: 52fdfc07-2182-154f-163f-5f0f9a621d72 Version: $LATEST
[INFO]	2019-03-09T18:51:44.232Z	52fdfc07-2182-154f-163f-5f0f9a621d72	{"event": {"body": "eyJ0ZXN0IjoiYm9keSJ9", "resource": "/{proxy+}", "path": "/path/to/resource", "httpMethod": "POST", "isBase64Encoded": true, "queryStringParameters": {"foo": "bar"}, "pathParameters": {"proxy": "/path/to/resource"}, "stageVariables": {"baz": "qux"}, "headers": {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Encoding": "gzip, deflate, sdch", "Accept-Language": "en-US,en;q=0.8", "Cache-Control": "max-age=0", "CloudFront-Forwarded-Proto": "https", "CloudFront-Is-Desktop-Viewer": "true", "CloudFront-Is-Mobile-Viewer": "false", "CloudFront-Is-SmartTV-Viewer": "false", "CloudFront-Is-Tablet-Viewer": "false", "CloudFront-Viewer-Country": "US", "Host": "1234567890.execute-api.us-east-1.amazonaws.com", "Upgrade-Insecure-Requests": "1", "User-Agent": "Custom User Agent String", "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)", "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==", "X-Forwarded-For": "127.0.0.1, 127.0.0.2", "X-Forwarded-Port": "443", "X-Forwarded-Proto": "https"}, "requestContext": {"accountId": "123456789012", "resourceId": "123456", "stage": "prod", "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef", "requestTime": "09/Apr/2015:12:34:56 +0000", "requestTimeEpoch": 1428582896000, "identity": {"cognitoIdentityPoolId": null, "accountId": null, "cognitoIdentityId": null, "caller": null, "accessKey": null, "sourceIp": "127.0.0.1", "cognitoAuthenticationType": null, "cognitoAuthenticationProvider": null, "userArn": null, "userAgent": "Custom User Agent String", "user": null}, "path": "/prod/path/to/resource", "resourcePath": "/{proxy+}", "httpMethod": "POST", "apiId": "1234567890", "protocol": "HTTP/1.1"}}, "x-application-trace-id": "d2ca8a85-6a7f-420b-abdb-30f4e75a0662"}
[INFO]	2019-03-09T18:51:44.233Z	52fdfc07-2182-154f-163f-5f0f9a621d72	{"result": {"statusCode": 200, "body": "{\"message\": \"hello world\"}", "headers": {"x-application-trace-id": "d2ca8a85-6a7f-420b-abdb-30f4e75a0662"}}, "x-application-trace-id": "d2ca8a85-6a7f-420b-abdb-30f4e75a0662"}
END RequestId: 52fdfc07-2182-154f-163f-5f0f9a621d72
REPORT RequestId: 52fdfc07-2182-154f-163f-5f0f9a621d72	Duration: 6.70 ms	Billed Duration: 100 ms	Memory Size: 128 MB	Max Memory Used: 22 MB
```
