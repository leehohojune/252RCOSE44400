# Use Python 3.13 base image for AWS Lambda
FROM public.ecr.aws/lambda/python:3.13

# Add the required commands here
# NOTE:
# (1) AWS Lambda container images use a fixed working directory called ${LAMBDA_TASK_ROOT}.
#     All source code and dependencies must be copied into this directory.
#
# (2) The Lambda handler must be specified using CMD in the form "filename.function_name".
#     This tells Lambda which function to call when the container is invoked.
#
# A Lambda handler is the entry point function executed by AWS Lambda.
# It receives two parameters: 'event' (input data) and 'context' (runtime information).
