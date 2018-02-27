node {
    def client = Artifactory.newConanClient()

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        client.run(command: "create . user/testing -s build_type=Debug")
    }
}