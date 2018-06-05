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

    stage('deploy to dev') {
      environment {
          ENVIRONMENT = 'dev'
      }
      steps {
        sh 'echo "deploy to ${ENVIRONMENT}..."'
        sh 'make deploy'
      }
    }

    stage('deploy to stg') {
      environment {
          ENVIRONMENT = 'stg'
      }
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'deploy to stg?', submitter: 'admin', submitterParameter: 'submitter'
        }
        sh 'export ENVIRONMENT=stg'
        sh 'make deploy'
        sh 'echo "deploy to ${ENVIRONMENT}..."'
      }
    }

    stage('deploy to prod') {
      environment {
          ENVIRONMENT = 'prod'
      }
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'deploy to prod?', submitter: 'admin', submitterParameter: 'submitter'
        }
        sh 'echo "deploy to ${ENVIRONMENT}..."'
        sh 'helm init'
      }
    }
  }
}
