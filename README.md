# S3 To LogEntries
This allows you to build AWS Lambda bundles (in .zip form) that will send
notifications of S3 activity to LogEntries.

Core based off [rapid7/le_lambda](https://github.com/rapid7/le_lambda)

###### Example use cases:
* Getting notified about database backups stored in S3

## Obtain log token(s)
1. Log in to your Logentries account
2. Add a new [token based log](https://logentries.com/doc/input-token/)

## Deploy the script on AWS Lambda
1. Create a new Lambda function

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step1.png)

2. Choose the Python blueprint for S3 objects

   ![Choose Blueprint](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step2.png)

3. Configure event sources:
   * Select S3 as event source type
   * Choose the bucket log files are being stored in
   * Set event type "Object Created (All)"

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step3.png)

4. Configure function:
   * Give your function a name
   * Set runtime to Python 2.7

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step4.png)

5. Create / Edit your .env.* file:
   * Create and/or edit a new `.env.*` file, i.e. `.env.my_app_backups`
     * `ENV_EXAMPLE` shows an example .env file
   * Build your `*.zip` file by running the `build.sh` script
     * Provide the `.env.*` file and optionally an output file name. i.e.:
       * `./build.sh -e .env.documentation -o backup_documentation`
   * Choose "Upload a .ZIP file" in AWS Lambda and upload the archive created in previous step

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step5.png)

6. Lambda function handler and role
   * Change the "Handler" value to ```le_lambda.lambda_handler```
   * Create a new S3 execution role (your IAM user must have sufficient permissions to create & assign new roles)

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step6.png)

7. Allocate resources:
   * Set memory and timeout appropriate for your use case.

8. Enable function:
   * Select "Enable now"
   * Click "Create function"

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step8.png)

   ![Create Function](https://raw.githubusercontent.com/logentries/le_lambda/master/doc/step9.png)
