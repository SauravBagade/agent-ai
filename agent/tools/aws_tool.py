# agent/tools/aws_tool.py

import subprocess
import boto3
import os


class AWSTool:
    """
    AWS Tool for interacting with AWS using both:
      - boto3 SDK (preferred for programmatic operations)
      - AWS CLI (preferred in DevOps pipelines)

    Supports:
      - EKS: list clusters, get kubeconfig
      - EC2: list instances
      - S3: list buckets
      - IAM: identity info
      - CloudWatch: logs + metrics (future)
    """

    def __init__(self, region: str = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")

        # boto3 clients
        self.eks = boto3.client("eks", region_name=self.region)
        self.ec2 = boto3.client("ec2", region_name=self.region)
        self.s3 = boto3.client("s3", region_name=self.region)
        self.iam = boto3.client("sts", region_name=self.region)

    # ---- EKS: LIST CLUSTERS ----

    def list_eks_clusters(self):
        try:
            resp = self.eks.list_clusters()
            return resp.get("clusters", [])
        except Exception as e:
            return f"[aws-error] {str(e)}"

    # ---- EKS: GET KUBECONFIG (CLI) ----

    def get_eks_kubeconfig(self, cluster: str):
        """
        Uses AWS CLI to fetch kubeconfig for EKS clusters.
        Equivalent:
          aws eks update-kubeconfig --name cluster --region region
        """
        cmd = [
            "aws", "eks", "update-kubeconfig",
            "--name", cluster,
            "--region", self.region
        ]
        return self._exec(cmd)

    # ---- EC2: LIST INSTANCES ----

    def list_ec2(self):
        try:
            resp = self.ec2.describe_instances()
            instances = []
            for reservation in resp.get("Reservations", []):
                for instance in reservation.get("Instances", []):
                    instances.append({
                        "id": instance.get("InstanceId"),
                        "type": instance.get("InstanceType"),
                        "state": instance.get("State", {}).get("Name"),
                        "private_ip": instance.get("PrivateIpAddress", None),
                        "public_ip": instance.get("PublicIpAddress", None),
                    })
            return instances
        except Exception as e:
            return f"[aws-error] {str(e)}"

    # ---- S3: LIST BUCKETS ----

    def list_s3_buckets(self):
        try:
            resp = self.s3.list_buckets()
            return [b["Name"] for b in resp.get("Buckets", [])]
        except Exception as e:
            return f"[aws-error] {str(e)}"

    # ---- IAM: WHOAMI ----

    def aws_identity(self):
        try:
            resp = self.iam.get_caller_identity()
            return {
                "account": resp.get("Account"),
                "user": resp.get("Arn"),
                "id": resp.get("UserId")
            }
        except Exception as e:
            return f"[aws-error] {str(e)}"

    # ---- INTERNAL EXEC (AWS CLI) ----

    def _exec(self, cmd):
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            return result.decode("utf-8").strip()
        except subprocess.CalledProcessError as e:
            return f"[aws-cli-error] {e.output.decode('utf-8').strip()}"
        except FileNotFoundError:
            return "[aws-cli-not-installed] AWS CLI not found."
