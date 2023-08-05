import subprocess
from pipeline.singleton import Singleton
from pipeline.helpers import execute


class Docker(object):
    __metaclass__ = Singleton

    def pull(self, image):
        return execute(f"docker pull {image}")

    def run(self, image, *commands, cwd=None, env_args="", options=""):
        self.pull(image)
        command = " ".join(arg for arg in commands)
        return execute(
            f"""docker run -it -v $(pwd):/home/src -w /home/src {env_args} {image} {command} {options}""",
            cwd,
        )
