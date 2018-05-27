pipeline {
  agent any
  stages {
    stage('docker build') {
      steps {
        sh 'make build'
        sh 'make test'
      }
    }
  }
}
