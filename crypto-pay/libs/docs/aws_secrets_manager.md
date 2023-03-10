# Guide to AWS Secrets Manager
AWS Secrets Manager is a service that stores and manages secrets securely. Our secrets are stored on AWS's server and can be accessed anywhere as long as we have the correct credentials.


## Part 1: Configuring AWS Credentials
Our Security Team have setup an **IAM user** specifically for QA Team in accessing AWS Secrets Manager. This set of credentials can only be used to view or modify secrets with id starts with `qa-automation/`.

You may find the credentials within our QA Team shared 1Password vault. Ask for assistance if you do not have access to the vault.
> Please be careful while handling the credentials. Giving this set of credentials to someone means giving them full control of our secrets.

The credentials file should be aptly named `credentials` (with no extension) and the content should look something like this:
```
[default]
aws_access_key_id = <some strings>
aws_secret_access_key = <some other strings>
```

Once you have the credentials, you may configure it on your device with the following options:

### Option A: Through AWS CLI (Recommended)
1. Install AWS CLI

    Install with brew if you are using MacOS and have [homebrew](https://brew.sh/) installed:
    ```sh
    brew install awscli
    ```
    > For other platforms, follow the instruction on https://aws.amazon.com/cli/.

    Check that AWS CLI is installed correctly:
    ```sh
    aws help
    ```
    You should see a manual on how to use this CLI.
    > By default the manual should be opened with vim in read-only mode. Press `q` to exit and return to terminal.

2. Configure the credentials

    Use the follow command:
    ```sh
    aws configure
    ```
    You should see it asking for `AWS Access Key ID` and `AWS Secret Access Key`.
    Enter the credentials accordingly.

    When it asks for `Default region name`, type in `ap-southeast-1`.

    When it asks for `Default output format`, you may either leave it blank, or type in `table` for human-friendly format that is more readable.

    > You may read more on the configuration in AWS CLI User Guide: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

### Option B: Directly modifying the configuration file
Simply paste the credentials file under `~/.aws/` directory. Create the directory if it does not exist.

The path of the file should now be `~/.aws/credentials`.

> Learn more on how the configuration settings were stored: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html


## Part 1.5: Checking the Credentials are setup correctly
With AWS CLI installed, use the following command:
```sh
aws sts get-caller-identity
```
You should see the details of our credentials, with an ARN ending in `:user/qa_automation`.

> If you are **only reading this in order to run our scripts** that use AWS Secrets Manager, you should be able to do so at this point and **should stop reading**. Otherwise, read on.


## Part 2: Working with Secrets
With the credentials correctly setup in your device, you should be able to manipulate the secrets stored within AWS Secrets Manager. You have a few options to do so:

### Option A: Through AWS CLI
With AWS CLI installed, you should be able to do the following:
#### Get a list of store secrets
```sh
aws secretsmanager list-secrets --filters Key=name,Values=qa-automation
```
#### Describe a specific secret
```sh
aws secretsmanager describe-secret --secret-id qa-automation/<id>
```
#### Retrieve a specific secret
```sh
aws secretsmanager get-secret-value --secret-id qa-automation/<id>
```
#### Create a new secret
```sh
aws secretsmanager create-secret --name qa-automation/<id> --description <description> --secret-string <value>
```
#### Modify a specific secret
```sh
aws secretsmanager update-secret --secret-id qa-automation/<id> --secret-string <value>
```
#### Delete a specific secret
```sh
aws secretsmanager delete-secret --secret-id qa-automation/<id> --force-delete-without-recovery
```
> Read the full list of the available commands here: https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/index.html

### Option B: Through Boto3(Python)
[Boto3](https://pypi.org/project/boto3/) is the AWS SDK for Python. It provides a client specifically for interacting with AWS Secrets Manager. Here are some examples:
#### Setting up the client
```py
import boto3

client = boto3.client("secretsmanager")
```
#### Get a list of store secrets
```py
response = client.list_secrets(Filters=[{"Key": "name", "Values": ["qa-automation"]}])
```
#### Describe a specific secret
```py
response = client.describe_secret(SecretId="qa-automation/<id>")
```
#### Retrieve a specific secret
```py
response = client.get_secret_value(SecretId="qa-automation/<id>")
```
#### Create a new secret
```py
response = client.create_secret(
    Name="qa-automation/<id>",
    Description="<description>",
    SecretString="<value>",
)
```
#### Modify a specific secret
```py
response = client.update_secret(
    SecretId="qa-automation/<id>",
    SecretString="<value>",
)
```
#### Delete a specific secret
```py
response = client.delete_secret(
    SecretId="qa-automation/<id>",
    ForceDeleteWithoutRecovery=True,
)
```
> Read the full list of the available methods here: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html

### Option C: Through 3rd Party Tools
There are a few 3rd party tools being developed to interact with AWS Secrets Manager. Here are some examples:
#### AWS Secrets Manager Explorer
https://github.com/kevcodez/aws-secrets-manager-explorer  
Simply download and run the GUI, following its instruction to setup a profile.

#### AWS Secrets Manager UI
https://github.com/ledongthuc/awssecretsmanagerui  
With docker installed, run the following command:
```docker
docker run -it --rm \
 -p 30301:30301 \
 -v $HOME/.aws:/root/.aws \
 ledongthuc/awssecretsmanagerui:unstable
```
You should be able to access the GUI on http://localhost:30301.
> Using a 3rd party tool may pose security risks. Use with discretion.


## Extra: Organizing Secrets
In order to better organize our secrets, considerations should be taken before adding new secrets to the Secrets Manager. Here are some suggestions to be considered:

1. Secrets with close relationship should be grouped in json and stored as secret string under a single entry.  
    e.g. Our Gmail tokens consist of `CLIENT_ID` and `CLIENT_SECRET`. They are composed into json and stored under the secret id of `qa-automation/gmail`.
    ```py
    client.get_secret_value(SecretId="qa-automation/gmail")
    >> {
        "CLIENT_ID": "some string",
        "CLIENT_SECRET": "some other string"
       }
    ```
2. Secrets that are specific to a project should be stored under its own directory to avoid collision with secrets from other projects.  
    e.g. Our tokens used specifically by the downloader of `crypto-app` is stored under the secret id of `qa-automation/crypto-app/downloader`. On the contrary, since our Gmail tokens are used across all projects and are not specific, they are stored simply as `qa-automation/gmail`.


## Further Reading
[Secrets Manager best practices](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
