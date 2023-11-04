#!/bin/bash

BAT=$(acpi -b | grep -E -o '[0-9][0-9][0-9]?%')
CHAR=$(acpi -b | grep -E -o 'Charging|Discharging')
LABEL="⚡"

if [ "$CHAR" = "Discharging" ]; then
   if [ ${BAT%?} -ge 50 ]; then
      LABEL="🔋"
   else
      LABEL="🪫"
   fi
fi

echo "$LABEL $BAT"

exit 0
