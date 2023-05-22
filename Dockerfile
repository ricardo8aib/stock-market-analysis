FROM public.ecr.aws/lambda/python:3.9-arm64

# Install the function's dependencies using file requirements.txt
COPY infrastructure/lambda-forecast/lambda_function/requirements.txt .
RUN  pip install -r requirements.txt

# Install extra requirements
RUN pip install pydantic[dotenv]
RUN pip install scikit-learn

# Create directories
RUN mkdir src
RUN mkdir src/forecast
RUN mkdir src/config
RUN touch src/__init__.py

# Copy source code
COPY infrastructure/lambda-forecast/lambda_function/app.py src/forecast/.
COPY src/forecast src/forecast/.
COPY src/config src/config/.
COPY .env .

# Define PYTHONPATH
ENV PYTHONPATH src/forecast

# Set the CMD to the handler
CMD [ "src.forecast.app.lambda_handler" ]