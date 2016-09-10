#!/bin/bash
# get the IP out so we can connect to lxd
# https://github.com/docker/docker/issues/1143#issuecomment-233152700
export HOST_IP=$(printf "%d." $(
  echo $(awk '$2 == "00000000" {print $3}' /proc/net/route) | sed 's/../0x& /g' | tr ' ' '\n' | tac
  ) | sed 's/\.$/\n/')