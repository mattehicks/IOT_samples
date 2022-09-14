#!/bin/bash


BUILD_DIR="/cm_data/disdnms/mms";
if [ ! -d "$BUILD_DIR" ]; then
	BUILD_DIR='.'
fi

export VERSION='0.1'
CLEAN_ARG='clean'
DO_RUN='1'
PROJ_ARG=''
SINGLE_ONLY='0'
OFFLINE_ARG='-o'
DEPLOY_ARGS=''

#NOTE:  ALL DATES IN UTC TIME !!!

#CONNECTING WITH SSH FORWARDING
# ssh variables
#host = '18.252.109.50'
host = '10.0.1.254'
localhost = 'localhost'
ssh_username = 'em7admin'
private_key = './matt.pem'

#VARIABLE NAMES FOR EMC APPS AND ENTITIES in SL1
missionval = "MP Mission"
planval = "MP Plan"
terminalval = "MP Terminal"
modemval = "MP Modem"
emsmodemval = "EMS Modem"
emscontrollerval = "EMS Controller"
emsemulatorval = "EMS Emulator"

fail()
{
	echo "$*"
	exit 1
}



while [ "$1" != '' ]; do
	# Consume the next option.
	OPT="$1"
	shift
	# Decode it.
	if [ "$OPT" = '-nostart' ]; then
		DO_STARTUP='0'
	elif [ "$OPT" = '-nocfg' ]; then
		DO_CFG='0'	


############################
# Invoke the Helper Scripts.
############################

if [ "$DO_CFG" = '1' ]; then
	./deploy-cfgs.sh $OPT_DRY -nostart $OPT_FORCE $OPT_BACKUPDIR $OPT_VARDIR $OPT_CFGDIR $OPT_WCFGDIR $OPT_WFBINDIR $CFG_LIST || fail "Failed to deploy configs."
else
	echo "Skipping configs."
fi



##################
# Startup The IOTMC Script.
##################

# Default the Wildfly PID to 0 to indicate it is not running.
WILDFLY_PID='0'
# Detect whether Wildfly is up, if possible.
if [ "$IS_NATIVE" = '1' ]; then
	# Detect whether Wildfly is up.
	WILDFLY_PID=`/share/mms/getmmspid.sh`
fi

if [ "$WILDFLY_PID" != '0' ]; then
	# Already started, so not applicable.
	DO_STARTUP='0'
fi

if [ "$DO_STARTUP" == '1' ]; then
	# Re/start JBOSS.
	/share/mms/startmms.sh
fi


echo "Deployment complete."

exit 0