#!/bin/sh
while true; do
	num=`ps -ef | grep "socat" | grep -v "grep" | wc -l`
	if [ $num -lt 5 ]; then
		socat tcp4-listen:10001,reuseaddr,fork exec:./a.out &
	fi
done
