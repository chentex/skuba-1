#!/usr/bin/env python3 

# !!!  This script is called by makefile only. !!!
# in root dir: make test-e2e

import subprocess
import os
import json

## ginkgobinary:
# assume the user as an installed binary from system if the env var isn't set
ginkgo_binary = "ginkgo"

# set ssh env
# the socket is setup with make setup-ssh, see setup-ssh.py
os.environ['SSH_AUTH_SOCK'] = "/tmp/ssh-agent-sock"

# we override the binary path by env variable. This is used by CI when we build ginkgo from vendor dir
#  see pipilines for more doc. IT can be used also locally
if "GINKGO_BIN_PATH" in os.environ:
  ginkgo_binary = os.environ['GINKGO_BIN_PATH']


# 1) set all IPS variable individually ( with the env. variables)
# 2) read this IPS from a tfstate which will set the env. variables.

if os.environ.get('IP_FROM_TF_STATE') == 'True' or os.environ.get('IP_FROM_TF_STATE') == 'TRUE':
  # we need to know which provider is beeing used to read the tfstates.
  if not "PLATFORM" in os.environ:
    raise(Exception("you need to set PLATFORM ENV. variable with LOAD_IP_FROM_TF_STATE env var"))

  tf = os.path.join("ci/infra/{0}".format(os.environ['PLATFORM'].lower()), "terraform.tfstate")
  with open(tf) as f:
    tf_state = json.load(f)

  # Vmware template return a list while OpenStack returns a String
  lb_ip = tf_state["modules"][0]["outputs"]["ip_load_balancer"]["value"]
  if isinstance(lb_ip, list):
    lb_ip = lb_ip[0]

  os.environ['CONTROLPLANE'] = lb_ip
  os.environ['MASTER00'] = tf_state["modules"][0]["outputs"]["ip_masters"]["value"][0]
  os.environ['WORKER00'] = tf_state["modules"][0]["outputs"]["ip_workers"]["value"][0]

subprocess.check_call("{0} -v --trace --progress test/core-features".format(ginkgo_binary), shell=True, env=dict(os.environ))
