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
          input 'Deploy to dev?'
        }
        sh 'echo "deploying..."'
      }
    }
  }
}
