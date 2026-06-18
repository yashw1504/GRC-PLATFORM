class CICDScore:

    @staticmethod
    def calculate(features):

        score = 0

        weights = {

            "sast": 10,

            "gitleaks": 10,

            "dependency_scan": 10,

            "container_scan": 10,

            "iac_scan": 10,

            "k8s_scan": 10,

            "sbom": 10,

            "security_gate": 10,

            "notifications": 5,

            "artifact_signing": 15
        }

        for k, v in weights.items():

            if features.get(k):
                score += v

        return score