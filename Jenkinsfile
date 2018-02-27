stage("create package") {
    def client = Artifactory.newConanClient()

    parallel
        linuxDebugStatic: {
            stage("Debug Static") {
                checkout scm
                client.run(command: "create . user/testing -s build_type=Debug -s Shared=False")
            }
        },
        linuxReleaseStatic: {
            stage("Release Static") {
                checkout scm
                client.run(command: "create . user/testing -s build_type=Release -s Shared=False")
            }
        },
        linuxDebugShared: {
            stage("Debug Shared") {
                checkout scm
                client.run(command: "create . user/testing -s build_type=Debug -s Shared=True")
            }
        },
        linuxReleaseShared: {
            stage("Release Shared") {
                checkout scm
                client.run(command: "create . user/testing -s build_type=Release -s Shared=True")
            }
        }
    }
}
