import boto3
import json

class LambdaAPI:
    def __init__(self, access_key: str, secret_key: str, region_name: str):
        self.lambda_client = boto3.client('lambda', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

    def create_function(self, function_name: str, handler: str, runtime: str, role: str, zip_file_path: str):
        with open(zip_file_path, 'rb') as f:
            zip_file_contents = f.read()
        response = self.lambda_client.create_function(FunctionName=function_name, Runtime=runtime, Role=role, Handler=handler, Code=dict(ZipFile=zip_file_contents))
        return response['FunctionArn']

    def update_function(self, function_name: str, zip_file_path: str):
        with open(zip_file_path, 'rb') as f:
            zip_file_contents = f.read()
        response = self.lambda_client.update_function_code(FunctionName=function_name, ZipFile=zip_file_contents)
        return response['FunctionArn']

    def list_functions(self):
        response = self.lambda_client.list_functions()
        return [func['FunctionName'] for func in response['Functions']]

    def invoke_function(self, function_name: str, payload: dict):
        response = self.lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(payload))
        return response['Payload'].read().decode('utf-8')

    def delete_function(self, function_name: str):
        self.lambda_client.delete_function(FunctionName=function_name)
        
 # Create an instance of the LambdaAPI class
lambda_api = LambdaAPI(access_key='your_access_key', secret_key='your_secret_key', region_name='your_region_name')

# Create a new Lambda function
function_name = 'my-new-function'
handler = 'handler.lambda_handler'
runtime = 'python3.9'
role = 'arn:aws:iam::your-account-id:role/your-role-name'
zip_file_path = '/path/to/lambda/function/zip/file'
function_arn = lambda_api.create_function(function_name=function_name, handler=handler, runtime=runtime, role=role, zip_file_path=zip_file_path)
print(f'Created Lambda function with ARN: {function_arn}')

# List all Lambda functions
print(lambda_api.list_functions())

# Update an existing Lambda function
new_zip_file_path = '/path/to/new/lambda/function/zip/file'
updated_function_arn = lambda_api.update_function(function_name=function_name, zip_file_path=new_zip_file_path)
print(f'Updated Lambda function with ARN: {updated_function_arn}')

# Invoke a Lambda function
payload = {'key': 'value'}
response = lambda_api.invoke_function(function_name=function_name, payload=payload)
print(f'Response from Lambda function: {response}')

# Delete a Lambda function
lambda_api.delete_function(function_name=function_name)
