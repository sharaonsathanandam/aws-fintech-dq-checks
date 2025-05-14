pipeline {
  agent any

  environment {
    AWS_DEFAULT_REGION = 'us-east-2'
    AWS_ACCESS_KEY_ID     = credentials('Terraform-CICD')
    AWS_SECRET_ACCESS_KEY = credentials('Terraform-CICD')
  }

  stages {

    stage('Migrate Glue Script from Git to S3 Location') {
      steps {
                sh '''
                    echo "Uploading Glue scripts to S3 bucket"
                    /usr/local/bin/aws s3 cp glue-scripts/* s3://fintech-glue-scripts/ --acl bucket-owner-full-control --include "*.py"
                  '''
            }
     }
  }
}
