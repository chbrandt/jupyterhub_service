c = get_config()  # noqa

# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

# Authenticator
from oauthenticator.gitlab import GitLabOAuthenticator
c.JupyterHub.authenticator_class = GitLabOAuthenticator

from dockerspawner import DockerSpawner
class CustomDockerSpawner(DockerSpawner):
    def options_from_form(self, formdata):
        options = {}
        image_form_list = formdata.get("image", [])
        if image_form_list and image_form_list[0]:
            options["image"] = image_form_list[0].strip()
            self.log.info(f"User selected image: {options['image']}")
        return options

    def load_user_options(self, options):
        image = options.get("image")
        if image:
            self.log.info(f"Loading image {image}")
            self.image = image

# c.JupyterHub.spawner_class = CustomDockerSpawner
c.JupyterHub.spawner_class = "docker"

options_form_tpl = """
<label for="image">
    Image
</label>
<input name="image"
    class="form-control"
    placeholder="the image to launch (default: {default_image})">
</input>
"""

def get_options_form(spawner):
    return options_form_tpl.format(default_image=spawner.image)

# c.DockerSpawner.options_form = get_options_form

# pick a default image to use when none is specified
c.DockerSpawner.image = "jupyter/base-notebook"

# delete containers when they stop
c.DockerSpawner.remove = True

# c.SingleUserNotebookApp.default_url = "/lab"
# c.Spawner.args = ['--NotebookApp.default_url=/lab']

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
# import os
# # notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
# notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
# c.DockerSpawner.notebook_dir = notebook_dir
#
# # Mount the real user's Docker volume on the host to the notebook user's
# # notebook directory in the container
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# c.Spawner.mem_limit = '3G'


# From: https://discourse.jupyter.org/t/dockerspawner-and-volumes-from-host/7008/6
#
# Spawn a new docker for each user
NOTEBOOK_DIR = '/home/jovyan/work'
HOST_HOME_PATH = "/tmp"
HOST_USER_PATH = HOST_HOME_PATH + "/{username}"
HOST_NOTEBOOK_PATH = f"{HOST_USER_PATH}/work"

# c.JupyterHub.spawner_class = "docker"
# c.DockerSpawner.image = os.environ["DOCKER_JUPYTER_IMAGE"]
# c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.notebook_dir = NOTEBOOK_DIR
c.DockerSpawner.remove = True
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_EXTRA": "/home/jovyan",
    "CHOWN_HOME_OPTS": "-R",
    "NB_UID": 1000,
    "NB_GID": 1000,
}

c.DockerSpawner.volumes = {
    f"{HOST_NOTEBOOK_PATH}": NOTEBOOK_DIR
}
