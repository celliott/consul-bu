pipeline {

  agent any

  stages {
    stage('docker build') {
      steps {
        sh 'make build'
      }
    }

    stage('docker test') {
      steps {
        sh 'make test'
      }
    }

    environment {
        ENVIRONMENT = 'dev'
    }

    stage('deploy to dev') {
      steps {
        sh 'echo "deploying to ${ENVIRONMENT}..."'
      }
    }

    environment {
        ENVIRONMENT = 'stg'
    }

    stage('deploy to stg') {
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'deploy to stg?', submitter: 'admin', submitterParameter: 'submitter'
        }
        sh 'export ENVIRONMENT=stg'
        sh 'echo "deploying to ${ENVIRONMENT}..."'
      }
    }

    environment {
        ENVIRONMENT = 'prod'
    }

    stage('deploy to prod') {
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'deploy to prod?', submitter: 'admin', submitterParameter: 'submitter'
        }
        sh 'echo "deploying to ${ENVIRONMENT}..."'
      }
    }
  }
}
