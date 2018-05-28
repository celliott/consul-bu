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
      steps {
        timeout(time: 1, unit: 'HOURS') {
          input message: 'deploy to dev?', submitter: 'admin', submitterParameter: 'submitter'
        }
        sh 'echo "deploying to dev..."'
      }
    }
  }
}
