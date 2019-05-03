library 'jenkins-ptcs-library@0.4.0'

podTemplate(label: pod.label,
  containers: pod.templates + [
  ]
) {
    def project = 'bittipannu-slack-integration'
    def branch = (env.BRANCH_NAME)
    def namespace = 'bittipannu-slack'

    node(pod.label) {
        try {
            stage('Checkout') {
                checkout scm
            }
            stage('ApplyToTestEnv') {
                if(env.BRANCH_NAME == 'master') {
                    def published = publishContainerToGcr(project);

                    toK8sTestEnv() {
                        sh """
                            kubectl set image deployment/$project-$branch $project-$branch=$published.image:$published.tag --namespace=$namespace
                        """
                    }
                    setPublicDnsToK8sTestEnv(
                        "bittipannu-slack-master.protacon.cloud"
                    )
                }
            }
        }
        catch (e) {
            currentBuild.result = "FAILED"
            throw e
        }
    }
  }