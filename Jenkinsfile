stage("create package") {
    parallel linux: {
        def client = Artifactory.newConanClient()

        node("Debug Static") {
            checkout scm
            client.run(command: "create . user/testing -s build_type=Debug -s Shared=False")
        },
        node("Release Static") {
            checkout scm
            client.run(command: "create . user/testing -s build_type=Release -s Shared=False")
        },
        node("Debug Shared") {
            checkout scm
            client.run(command: "create . user/testing -s build_type=Debug -s Shared=True")
        },
        node("Release Shared") {
            checkout scm
            client.run(command: "create . user/testing -s build_type=Release -s Shared=True")
        }
    }
}
