# Use Python 3.13 base image for AWS Lambda
FROM public.ecr.aws/lambda/python:3.13

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

RUN python -m textblob.download_corpora

COPY lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]
