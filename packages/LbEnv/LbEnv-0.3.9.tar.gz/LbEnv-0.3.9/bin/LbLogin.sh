#!/usr/bin/printf you must "source %s"\n
###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
# Backward compatibility wrapper for scripts relying on LbLogin.sh in the path
if [ -r "$MYSITEROOT/LbEnv.sh" ] ; then
  unset LBENV_SOURCED
  source $MYSITEROOT/LbEnv.sh "$@"
fi
