pipeline {
    stages {
        stage('Parallel steps') {
            parallel {
                stage('Linux Debug Static') {
                    steps {
                        def client = Artifactory.newConanClient()
                        checkout scm
                        client.run(command: "create . user/testing -s build_type=Debug -s Shared=False")
                    }
                }
                stage('Linux Debug Shared') {
                    steps {
                        def client = Artifactory.newConanClient()
                        checkout scm
                        client.run(command: "create . user/testing -s build_type=Debug -s Shared=True")
                    }
                }
                stage('Linux Release Static') {
                    steps {
                        def client = Artifactory.newConanClient()
                        checkout scm
                        client.run(command: "create . user/testing -s build_type=Release -s Shared=False")
                    }
                }
                stage('Linux Release Shared') {
                    steps {
                        def client = Artifactory.newConanClient()
                        checkout scm
                        client.run(command: "create . user/testing -s build_type=Release -s Shared=True")
                    }
                }
            }
        }
    }
}
