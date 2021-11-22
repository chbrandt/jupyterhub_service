# jupyterhub_service

JupyterHub spawner. A Jupyter lab/notebooks launcher after authenticating users.
A JupyterHub can spawn Notebooks as the server sections, or in docker containers.
We will set the containers system.


## Install

To install JupyterHub with conda:

```bash
$ conda create -n jupyterhub -c conda-forge -y jupyterhub[=1.4.1]
$ conda activate jupyterhub
$ pip install jupyter-client
$ pip install oauthenticator
$ pip install dockerspawner
```

After that, we want to config the system.

## References

- https://jupyterhub-dockerspawner.readthedocs.io/en/latest/
  * https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
  * https://github.com/jupyterhub/dockerspawner/blob/master/examples/image_form/jupyterhub_config.py
