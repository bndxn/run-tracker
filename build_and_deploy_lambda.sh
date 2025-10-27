# # Build and push the image to ECR

# docker buildx build --platform linux/amd64 --output type=docker,dest=amd64-image.tar -t fetch-and-suggest-lambda -f lambda.Dockerfile .
# docker load -i amd64-image.tar
# docker tag fetch-and-suggest-lambda 685541680156.dkr.ecr.eu-west-2.amazonaws.com/fetch-and-suggest-lambda:latest
# aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 685541680156.dkr.ecr.eu-west-2.amazonaws.com
# docker push 685541680156.dkr.ecr.eu-west-2.amazonaws.com/fetch-and-suggest-lambda:latest
# rm amd64-image.tar

# # Create lambda

# aws lambda create-function \
#   --function-name fetch-and-suggest \
#   --package-type Image \
#   --code ImageUri=685541680156.dkr.ecr.eu-west-2.amazonaws.com/fetch-and-suggest-lambda:latest \
#   --role arn:aws:iam::685541680156:role/run-tracker-fetch-and-suggest-lambda \
#   --region eu-west-2

# # Add in env variables

# aws lambda update-function-configuration \
#   --function-name fetch-and-suggest \
#   --timeout 600 \
#   --memory-size 512 \
#   --region eu-west-2

# # Create lambda trigger, requires rule, then event target (?), then add permission for the trigger to invoke the lambda

# aws events put-rule \
#   --name every-6-hours-lambda-trigger \
#   --schedule-expression "cron(0 0/6 * * ? *)" \
#   --region eu-west-2

# aws events put-targets \
#   --rule every-6-hours-lambda-trigger \
#   --targets "Id"="1","Arn"="arn:aws:lambda:eu-west-2:685541680156:function:create-function"

# aws lambda add-permission \
#   --function-name fetch-and-suggest \
#   --statement-id every-6-hours-eventbridge-trigger \
#   --action 'lambda:InvokeFunction' \
#   --principal events.amazonaws.com \
#   --source-arn arn:aws:events:eu-west-2:685541680156:rule/every-6-hours-lambda-trigger

# Build and push the web app image to ECR

docker buildx build --platform linux/amd64 --output type=docker,dest=amd64-image.tar -t run-tracker -f web_app.Dockerfile .
docker load -i amd64-image.tar
docker tag run-tracker 685541680156.dkr.ecr.eu-west-2.amazonaws.com/run-tracker:latest
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 685541680156.dkr.ecr.eu-west-2.amazonaws.com
docker push 685541680156.dkr.ecr.eu-west-2.amazonaws.com/run-tracker:latest
rm amd64-image.tar
