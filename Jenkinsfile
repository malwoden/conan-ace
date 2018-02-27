pipeline {
    stages {
        stage('Parallel steps') {
            parallel {
                stage('Linux Debug Static') {
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Debug -s Shared=False")
                        }
                    }
                }
                stage('Linux Debug Shared') {
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Debug -s Shared=True")
                        }
                    }
                }
                stage('Linux Release Static') {
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Release -s Shared=False")
                        }
                    }
                }
                stage('Linux Release Shared') {
                    steps {
                        checkout scm
                        script {
                            def client = Artifactory.newConanClient()
                            client.run(command: "create . user/testing -s build_type=Release -s Shared=True")
                        }
                    }
                }
            }
        }
    }
}
