"""Cloud scanner - uses stored credentials to audit cloud infrastructure"""
import os
from grc_scanner.scanners.base_scanner import BaseScanner
from grc_scanner.engine.finding import Finding
from grc_scanner.engine.risk_engine import RiskEngine
from grc_scanner.storage.credential_vault import CredentialVault

class AWSCloudScanner(BaseScanner):
    def __init__(self):
        self.name = "AWSCloudScanner"

    def scan(self, cred_id=None, **kwargs):
        findings = []

        # Get credentials from vault or env vars
        if cred_id:
            creds = CredentialVault.get_credential(cred_id)
            if not creds or creds["provider"] != "aws":
                print("[AWSCloudScanner] Invalid credential ID or not AWS")
                return findings
            aws_creds = creds["credentials"]
            os.environ["AWS_ACCESS_KEY_ID"] = aws_creds.get("aws_access_key_id", "")
            os.environ["AWS_SECRET_ACCESS_KEY"] = aws_creds.get("aws_secret_access_key", "")
            os.environ["AWS_DEFAULT_REGION"] = aws_creds.get("region", "us-east-1")
        elif os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            pass  # Use env vars
        else:
            print("[AWSCloudScanner] No AWS credentials available")
            return findings

        try:
            import boto3
            # Check S3 buckets
            s3 = boto3.client("s3")
            buckets = s3.list_buckets().get("Buckets", [])
            for bucket in buckets:
                try:
                    acl = s3.get_public_access_block(Bucket=bucket["Name"])
                    pub_block = acl.get("PublicAccessBlockConfiguration", {})
                    if not pub_block.get("BlockPublicAcls", False):
                        findings.append(RiskEngine.enrich_finding(Finding(
                            check_id="s3_public_acls",
                            name=f"S3 Bucket {bucket['Name']} allows public ACLs",
                            status="fail",
                            severity="High",
                            description="S3 bucket does not block public ACLs",
                            evidence=f"s3://{bucket['Name']}",
                            category="Cloud Security",
                            target_asset=bucket["Name"],
                            scanner_name="aws_cloud_scanner",
                            remediation="Enable BlockPublicAcls on the S3 bucket"
                        )))
                except:
                    pass

            # Check Security Groups
            ec2 = boto3.client("ec2")
            sgs = ec2.describe_security_groups()["SecurityGroups"]
            for sg in sgs:
                for perm in sg.get("IpPermissions", []):
                    for ip_range in perm.get("IpRanges", []):
                        if ip_range.get("CidrIp") == "0.0.0.0/0":
                            if perm.get("FromPort") == 22:
                                findings.append(RiskEngine.enrich_finding(Finding(
                                    check_id="sg_ssh_open_to_world",
                                    name=f"Security Group {sg['GroupName']} has SSH open to 0.0.0.0/0",
                                    status="fail",
                                    severity="Critical",
                                    description="SSH (port 22) is open to the entire internet",
                                    evidence=f"{sg['GroupName']} ({sg['GroupId']})",
                                    category="Cloud Security",
                                    target_asset=sg["GroupName"],
                                    scanner_name="aws_cloud_scanner",
                                    remediation="Restrict SSH access to specific IPs only"
                                )))

        except Exception as e:
            print(f"[AWSCloudScanner] Error: {e}")

        return findings


class AzureCloudScanner(BaseScanner):
    def __init__(self):
        self.name = "AzureCloudScanner"

    def scan(self, cred_id=None, **kwargs):
        findings = []

        if cred_id:
            creds = CredentialVault.get_credential(cred_id)
            if not creds or creds["provider"] != "azure":
                return findings
            az_creds = creds["credentials"]
            os.environ["AZURE_CLIENT_ID"] = az_creds.get("client_id", "")
            os.environ["AZURE_CLIENT_SECRET"] = az_creds.get("client_secret", "")
            os.environ["AZURE_TENANT_ID"] = az_creds.get("tenant_id", "")
            os.environ["AZURE_SUBSCRIPTION_ID"] = az_creds.get("subscription_id", "")

        if not all([os.getenv("AZURE_CLIENT_ID"), os.getenv("AZURE_CLIENT_SECRET")]):
            print("[AzureCloudScanner] No Azure credentials")
            return findings

        try:
            from azure.identity import ClientSecretCredential
            from azure.mgmt.security import SecurityCenter
            # Placeholder - Azure SDK integration here
            print("[AzureCloudScanner] Azure scanning ready (extend with specific checks)")
        except Exception as e:
            print(f"[AzureCloudScanner] Error: {e}")

        return findings


class GCPCloudScanner(BaseScanner):
    def __init__(self):
        self.name = "GCPCloudScanner"

    def scan(self, cred_id=None, **kwargs):
        findings = []
        print("[GCPCloudScanner] GCP scanning - extend with google-cloud-sdk integration")
        return findings