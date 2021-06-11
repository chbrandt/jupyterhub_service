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

c.JupyterHub.spawner_class = CustomDockerSpawner

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

c.DockerSpawner.options_form = get_options_form

# pick a default image to use when none is specified
c.DockerSpawner.image = "jupyter/base-notebook"

# delete containers when they stop
c.DockerSpawner.remove = True

# c.SingleUserNotebookApp.default_url = "/lab"
c.Spawner.args = ['--NotebookApp.default_url=/lab']

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
import os
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { '/tmp/jupyterhub-user-{username}': notebook_dir }

c.Spawner.mem_limit = '3G'
