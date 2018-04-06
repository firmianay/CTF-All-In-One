socat tcp4-listen:10001,reuseaddr,fork exec:"env LD_PRELOAD=./libc.so_1 ./freenote" &
