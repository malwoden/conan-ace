pipeline {
    agent none
    stages {
        stage('Parallel steps') {
            parallel {
                stage('Linux Debug Static') {
                    agent any
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Debug -o shared=False")
                        }
                    }
                }
                stage('Linux Debug Shared') {
                    agent any
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Debug -o shared=True")
                        }
                    }
                }
                stage('Linux Release Static') {
                    agent any
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Release -o shared=False")
                        }
                    }
                }
                stage('Linux Release Shared') {
                    agent any
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Release -o shared=True")
                        }
                    }
                }
            }
        }
    }
}
