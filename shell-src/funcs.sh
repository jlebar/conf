#!/bin/bash
# To be included by scripts that need these functions

# Red STDERR
# rse <command string>
#function rse()
#{
	# We need to wrap each phrase of the command in quotes to preserve arguments that contain whitespace
	# Execute the command, swap STDOUT and STDERR, colour STDOUT, swap back
#	((eval $(for phrase in "$@"; do echo -n "'$phrase' "; done)) 3>&1 1>&2 2>&3 | sed -e "s/^\(.*\)$/$(echo -en \\033)[31;1m\1$(echo -en \\033)[0m/") 3>&1 1>&2 2>&3
#}

function ff()
{
  dir=$($CONFDIR/bin/moz/ff $@)
  if [[ "$?" == 0 ]]; then
    cd $dir
  fi
}
