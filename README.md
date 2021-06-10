# jupyterhub_service

JupyterHub spawning

## Install

Let's install JupyterHub with conda:

```bash
$ conda create -n jupyterhub -c conda-forge -y jupyterhub
$ conda activate jupyterhub
$ pip install jupyter-client
$ pip install oauthenticator
$ pip install dockerspawner
```


## References

- https://jupyterhub-dockerspawner.readthedocs.io/en/latest/
  * https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
  * https://github.com/jupyterhub/dockerspawner/blob/master/examples/image_form/jupyterhub_config.py
