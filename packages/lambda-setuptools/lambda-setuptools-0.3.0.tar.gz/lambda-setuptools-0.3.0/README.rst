lambda-setuptools
=================

A Command extension to setuptools that builds an AWS Lambda compatible zip file and uploads it to an S3 bucket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply add ``setup_requires=['lambda_setuptools']`` as an attribute to
your *setup.py* file

This extension adds two new commands to setuptools:

1. **ldist**

   -  Usage:
      ``ldist --include-version=<True | true | Yes | yes | False | false | No | no>``

      -  Effect: This will build (using *bdist\_wheel*) and install your
         package, along with all of the dependencies in
         *install\_requires*

         -  *include-version* is optional. If not present it will
            default to *True*
         -  It is *highly* recommended that you **DO NOT** include
            *boto3* or *botocore* in your *install\_requires*
            dependencies as these are provided by the AWS Lambda
            environment. Include them at your own peril!
         -  The result will be in
            *dist/[your-package-name]-[version].zip* (along with your
            wheel)

2. **lupload**

   -  Usage:
      ``lupload --access-key=<my_access_key> --secret-access-key=<my_secret> --s3-bucket=<my_S3_bucket> --kms-key-id=<my_KMS_key> --s3-prefix=<my_S3_key_prefix> --endpoint-url=<my_endpoint_url>``

      -  Effect: This will build (using *ldist*) and upload the
         resulting ZIP file to the specified S3 bucket

         -  *kms-key-id* is optional. If it is not provided, standard
            AES256 encryption will be used
         -  *s3-prefix* is optional. If it is not provided, the ZIP file
            will be uploaded to the root of the S3 bucket
         -  *endpoint\_url* is optional. If it is not provided, the
            default endpoint for the accessed account will be used

3. **lupdate**

   -  Usage:
      ``lupdate --function-names=<my_function1>,<my_function2>,<my_function3> --region=<my_aws_region>``

      -  Effect: This will update the AWS Lambda function code for the
         listed functions. Functions may be function names, partial ARNs
         and/or full ARNs.

         -  Requires the use of *lupload* parameters as the S3 object
            uploaded is used as the function code to update.
         -  *region* is optional. If it is not provided, then
            ``us-east-1`` will be used.

This extension also adds three new attributes to the setup() function:

1. **lambda\_function**

   -  Usage:
      ``lambda_function=<my_package>.<some_module>:<some_function>``
   -  Effect: ldist will create a root-level python module named
      \*\_function.py\* where package\_name is derived from the *name*
      attribute. This created module will simply redefine your lambda
      handler function at the root-level

2. **lambda\_module**

   -  Usage: ``lambda_module=<some_module>``
   -  Effect: ldist adds the named module to the list of *py\_modules*
      to install, normally at the root level

3. **lambda\_package**

   -  Usage: ``lambda_package=<some_dir>``
   -  Effect: ldist will copy the contents of the provided directory
      into the root level of the resulting lambda distribution. The
      provided directory **MUST NOT** have an \*\_\_init\_\_.py\* in it
      (e.g. - it can't be a real package)

All *ldist* attributes can be used in the same setup() call. It is up to
the user to ensure that you don't step all over yourself...

Note that all other commands and attributes in setup.py will still work
the way you expect them to.

Enjoy!
