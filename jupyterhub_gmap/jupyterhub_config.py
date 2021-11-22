import os

c = get_config()  # noqa

# The docker instances need access to the Hub, so the default loopback port doesn't work:
from jupyter_client.localinterfaces import public_ips
c.JupyterHub.hub_ip = public_ips()[0]

# Authenticator
if 'GITLAB_HOST' in os.environ:
    from oauthenticator.gitlab import GitLabOAuthenticator
    c.JupyterHub.authenticator_class = GitLabOAuthenticator
# else:
#     from jupyterhub.auth import LocalAuthenticator
#     c.JupyterHub.authenticator_class = LocalAuthenticator

c.JupyterHub.spawner_class = "docker"

# pick a default image to use when none is specified
c.DockerSpawner.image = "jupyter:isis"

# delete containers when they stop
c.DockerSpawner.remove = True

# Use Lab as the default interface
# c.SingleUserNotebookApp.default_url = "/lab"
c.Spawner.args = ['--NotebookApp.default_url=/lab']

# # Explicitly set notebook directory because we'll be mounting a host volume to
# # it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# # user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# # We follow the same convention.
# # notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan'
# notebook_dir = '/home/jovyan/work'
# c.DockerSpawner.notebook_dir = notebook_dir
#
# # Mount the real user's Docker volume on the host to the notebook user's
# # notebook directory in the container
# c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

HOST_ISISDATA_PATH = os.environ['ISISDATA']
ISISDATA_PATH = '/isis/data'
# c.DockerSpawner.volumes = { ISISDATA : '/opt/conda/envs/isis/data' }
# c.DockerSpawner.volumes = { ISISDATA : '/isis/data' }

# Memory limit
# c.Spawner.mem_limit = '3G'

# From: https://discourse.jupyter.org/t/dockerspawner-and-volumes-from-host/7008/6
#
# Spawn a new docker for each user
c.JupyterHub.spawner_class = "docker"
c.DockerSpawner.image = "jupyter:isis"
c.DockerSpawner.remove = True
# c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]

HOST_HOME_PATH = "/tmp"
HOST_USER_PATH = HOST_HOME_PATH + "/{username}"
HOST_NOTEBOOK_PATH = f"{HOST_USER_PATH}/work"

# > HOST_NOTEBOOK_PATH should exist already.

NOTEBOOK_DIR = '/home/jovyan/work'

c.DockerSpawner.notebook_dir = NOTEBOOK_DIR

c.DockerSpawner.volumes = {
    f"{HOST_NOTEBOOK_PATH}": NOTEBOOK_DIR,
    f"{HOST_ISISDATA_PATH}": ISISDATA_PATH
}

c.DockerSpawner.extra_create_kwargs = {'user': 'root'}
c.DockerSpawner.environment = {
    "CHOWN_HOME": "yes",
    "CHOWN_EXTRA": "/home/jovyan",
    "CHOWN_HOME_OPTS": "-R",
    "NB_UID": 1000,
    "NB_GID": 100,
}

# Use Lab as the default interface
# c.SingleUserNotebookApp.default_url = "/lab"
c.Spawner.args = ['--NotebookApp.default_url=/lab']
