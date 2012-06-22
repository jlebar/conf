# Run with:
#  . set-path.sh

NEWPATH=`python $CONFDIR/shell-src/generate-path.py`

if [[ -n "$NEWPATH" ]] ; then
  export PATH="$NEWPATH"
  hash -r
fi

unset NEWPATH
