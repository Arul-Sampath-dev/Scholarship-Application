pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github-cred',
                        url: 'https://github.com/Arul-Sampath-dev/Scholarship-Application.git'
                    ]]
                )
            }
        }
    }
}
