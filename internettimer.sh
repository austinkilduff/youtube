# Boost productivity by shutting off the internet between the hours of 10pm and 6am
# This code snippet can be used for a cron job or any other repeatedly running script
#!/bin/sh

HOUR="$(date +%H 2>/dev/null)"
NETSTATUS="$(nmcli networking 2>/dev/null)"

if [ "$HOUR" -lt "6" ] || [ "$HOUR" -ge "22" ]
then
	case "$NETSTATUS" in
		enabled) nmcli networking off ;;
	esac
else
	case "$NETSTATUS" in
		disabled) nmcli networking on ;;
	esac
fi
