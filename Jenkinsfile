pipeline {
    agent none
    stages {
        stage('Parallel steps') {
            parallel {
                stage('Page 1/4') {
                    agent any
                    steps {
                        cleanWs()
                        checkout scm
                        script {
                            sh "CONAN_TOTAL_PAGES=4 CONAN_CURRENT_PAGE=1 python build.py"
                        }
                    }
                }
                stage('Page 2/4') {
                    agent any
                    steps {
                        cleanWs()
                        checkout scm
                        script {
                            sh "CONAN_TOTAL_PAGES=4 CONAN_CURRENT_PAGE=2 python build.py"
                        }
                    }
                }
                stage('Page 3/4') {
                    agent any
                    steps {
                        cleanWs()
                        checkout scm
                        script {
                            sh "CONAN_TOTAL_PAGES=4 CONAN_CURRENT_PAGE=3 python build.py"
                        }
                    }
                }
                stage('Page 4/4') {
                    agent any
                    steps {
                        cleanWs()
                        checkout scm
                        script {
                            sh "CONAN_TOTAL_PAGES=4 CONAN_CURRENT_PAGE=4 python build.py"
                        }
                    }
                }
            }
        }
    }
}
