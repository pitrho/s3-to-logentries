#!/bin/bash

OUTPUT_ZIP_FILE_NAME="s3_to_logentries"
ENV_FILE_NAME=""

# Custom die function.
#
die() { echo >&2 -e "\nRUN ERROR: $@\n"; exit 1; }

# Parse the command line flags.
#
while getopts "o:e:" opt; do
  case $opt in
    o)
      OUTPUT_ZIP_FILE_NAME=${OPTARG}
      ;;

    e)
      ENV_FILE_NAME=${OPTARG}
      ;;

    \?)
      die "Invalid option: -$OPTARG"
      ;;
  esac
done

if [ -z $ENV_FILE_NAME ]; then
  die "Please specify the .env.* file to use for building the config."
fi

# Grab our .env.* file to access variables
source $ENV_FILE_NAME

# Create our .py file we'll bundle
cp le_config.tmpl le_config.py

# Replace vars inside our tmpl file
# Kind of clunky for now b/c there are so few variables we're setting...
sed -i -e "s/log_token=.*/log_token=\"$log_token\"/" le_config.py
sed -i -e "s/send_body=.*/send_body=$send_body/" le_config.py
sed -i -e "s/size_as_mb=.*/size_as_mb=$size_as_mb/" le_config.py
sed -i -e "s/log_type_name=.*/log_type_name=\"$log_type_name\"/" le_config.py

# Create our zipped bundle
zip -R "${OUTPUT_ZIP_FILE_NAME}.zip" 'le_certs.pem' 'le_config.py' 'le_lambda.py'

# Clean up our resultant le_config.py file, which may contain secrets
rm le_config.py
rm le_config.py-e
