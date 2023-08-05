import subprocess
from lib_pipeline.docker import Docker
from lib_pipeline.singleton import Singleton
from lib_pipeline.helpers import execute, remove_files


class Terraform(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.docker = Docker()
        self.image = "hashicorp/terraform:light"
        self.env_args = '-v $HOME/.aws:/home/.aws'

    def exec(self, command, options='', cwd=None, env_args=''):
        options = " ".join(options)
        if env_args == '':
            env_args = self.env_args
        self.docker.run(
            self.image, command, options=options, cwd=cwd, env_args=env_args)

    def init(self, bucket, region, environment, backend_config='', cwd=None, env_args=''):
        self.exec("init", options=backend_config, cwd=cwd, env_args=env_args)

    def plan(self, region, environment, options, cwd=None, env_args=''):
        vars = [
            f"""--var-file="{environment}/{region}.tfvars" """,
            f"""--var="profile={environment}" {options} """,
        ]
        self.exec("plan", options=vars, cwd=cwd, env_args=env_args)

    def apply(self, region, environment, options, cwd=None, env_args=''):
        vars = [
            f"""--var-file="{environment}/{region}.tfvars" """,
            f"""--var="profile={environment}" {options} """,
            "--auto-approve",
        ]
        self.exec("apply", options=vars, cwd=cwd, env_args=env_args)

    def taint(self, bucket, region, environment, *args, backend_config='', cwd=None, env_args=''):
        options = " ".join(args)
        self.init(bucket, region, environment, options, backend_config=backend_config, cwd=cwd, env_args=env_args)
        self.plan(region, environment, options, cwd=cwd, env_args=env_args)
        self.exec("taint", options=options, cwd=cwd, env_args=env_args)

    def deploy(self, bucket, region, environment, *args, backend_config='', cwd=None, env_args=''):
        options = " ".join(args)
        remove_files(".terraform", cwd=cwd)
        self.init(bucket, region, environment, backend_config=backend_config, cwd=cwd, env_args=env_args)
        self.plan(region, environment, options, cwd=cwd, env_args=env_args)
        self.apply(region, environment, options, cwd=cwd, env_args=env_args)
