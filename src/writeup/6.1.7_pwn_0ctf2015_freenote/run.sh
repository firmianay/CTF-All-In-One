socat tcp4-listen:10001,reuseaddr,fork exec:"env LD_PRELOAD=./libc-2.19.so ./freenote" &
