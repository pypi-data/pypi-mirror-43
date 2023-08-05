from lib_pipeline.helpers import execute
import json


class AWS:
    def run(self, resource, command, cwd=None):
        return execute(f"aws {resource} {command}", cwd)


class S3(AWS):
    def __init__(self):
        self.resource = "s3"

    def copy(self, bucket_path, files, *args, **kwargs):
        options = " ".join(arg for arg in args)
        cwd = kwargs.get("cwd")
        return self.run(
            self.resource, f"cp {files} s3://{bucket_path} {options}", cwd=cwd
        )

    def empty(self, bucket_path, *args):
        options = " ".join(arg for arg in args)
        return self.run(self.resource, f"rm s3://{bucket_path} {options}")


class Route53(AWS):
    def __init__(self):
        self.resource = "route53"

    def list_resource_record_sets(self, hosted_zone_id, *args):
        options = " ".join(arg for arg in args)
        return self.run(
            self.resource,
            f"list-resource-record-sets --hosted-zone-id {hosted_zone_id} {options}",
        )

    def get_active_region(self, hosted_zone_id, dns_prefix, domain, *args):
        result = self.list_resource_record_sets(hosted_zone_id, *args)
        for i in json.loads(result.stdout)["ResourceRecordSets"]:
            if i["Name"] == f"{dns_prefix}.{domain}." and i["Failover"] == "PRIMARY":
                return i["SetIdentifier"].split("enterprise401k-marketing-site-")[1]
        return None
