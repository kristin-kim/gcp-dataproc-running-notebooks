#!/bin/bash

set -exo pipefail

# readonly PACKAGES=$(/usr/share/google/get_metadata_value attributes/PIP_PACKAGES || true)
PACKAGES="pendulum scipy markdown"

function err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
  exit 1
}

function run_with_retry() {
  local -r cmd=("$@")
  for ((i = 0; i < 10; i++)); do
    if "${cmd[@]}"; then
      return 0
    fi
    sleep 5
  done
  err "Failed to run command: ${cmd[*]}"
}

function install_pip() {
  if command -v pip >/dev/null; then
    echo "pip is already installed."
    return 0
  fi

  if command -v easy_install >/dev/null; then
    echo "Installing pip with easy_install..."
    run_with_retry easy_install pip
    return 0
  fi

  echo "Installing python-pip..."
  run_with_retry apt update
  run_with_retry apt install python-pip -y
}

function gcsfuse_install(){
  echo "Installing gcsfuse..."
  export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
  echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

  sudo apt-get update
  echo "-------apt-get update install + auto Yes added "
  sudo apt-get install gcsfuse -y

  sudo groupadd fuse
  sudo usermod -a -G fuse $USER

  echo $USER
  echo "-------Installed gcsfuse successfully"
}

function gcsfuse_mount(){  
  # Mount your bucket by “gcsfuse <bucket-name> </path/to/mount>”
  mkdir path-1
  gcsfuse kristin-0105 path-1
  echo "------- GCS succesfully mounted at path-1"

  mkdir path-2
  gcsfuse notebooks-staging-bucket-kk path-2
  echo "------- GCS succesfully mounted at path-2"
}

function gcsfuse_check(){
  # Check the mounted storage bucket as persistent disk by “df -h”
  df -h 
}

function main() {
  # if [[ -z "${PACKAGES}" ]]; then
  #   echo "ERROR: Must specify PIP_PACKAGES metadata key"
  #   exit 1
  # fi

  # install_pip
  # pip3 install --upgrade ${PACKAGES}
  run_with_retry pip install --upgrade ${PACKAGES}

  run_with_retry gcsfuse_install
  run_with_retry gcsfuse_mount
  run_with_retry gcsfuse_check
}

main