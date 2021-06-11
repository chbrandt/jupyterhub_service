#!/bin/bash
set -ue

source env.rc

CONFIG="$1"

sudo env PATH=$PATH \
     OAUTH_CALLBACK_URL=$OAUTH_CALLBACK_URL \
     OAUTH_CLIENT_ID=$OAUTH_CLIENT_ID \
     OAUTH_CLIENT_SECRET=$OAUTH_CLIENT_SECRET \
     GITLAB_HOST=$GITLAB_HOST \
     ISISDATA=$ISISDATA \
     jupyterhub --debug -f "$CONFIG" --port=8000

