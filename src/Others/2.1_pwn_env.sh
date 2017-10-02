#!/bin/bash
# usage: ./2.1_pwn_env.sh [func1[ func2[ func3...]]]
# tested for debian wheezy on armhf
# from Icemakr

function check_result() {
    if [ $? -ne 0 ]
    then
        res="\033[32m[-]failed to "$1"\033[0m"
        echo -e $res
    else
        res="\033[33m[+]successfully "$1"\033[0m"
        echo -e $res
    fi
}


############################# install ################################
######################################################################
######################################################################


# install vim, git, gcc, python
function init {
    #sudo apt-get update
    #check_result "update apt"

    sudo apt-get install git gcc
    sudo apt-get install python-dev python-pip
    check_result "install python"
    sudo apt-get install python3 python3-pip
    check_result "install python3"

	sudo apt-get install zsh
    check_result "install zsh"
}

# set up oh-my-zsh
function oh-my-zsh {
	sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)" && sudo chsh -s /bin/zsh
    check_result "install oh-my-zsh"
}

# set up vim
function vim {
    echo -e "set encoding=utf-8\nset fileencoding=utf-8\nset fileencodings=ucs-bom,utf-8,chinese,cp936\nset guifont=Consolas:h15\nlanguage messages zh_CN.utf-8\nset number\nset autoindent\nset smartindent\nset tabstop=4\nset autochdir\nset shiftwidth=4\nset foldmethod=manual\nsyntax enable\nset nocompatible\nset nobackup\ninoremap jk <ESC>" > ~/.vimrc && sudo apt-get install vim
    check_result "vim"
}

# install pwn
function pwn {
    sudo apt-get install gdb
    check_result "install gdb"
    sudo pip install zio
    check_result "install zio"
    sudo pip install pwntools
    check_result "install pwntools"
    sudo apt-get install socat
    check_result "install socat"
}

# install capstone
function capstone {
	sudo pip install capstone
	sudo pip3 install capstone
	check_result "install capstone-engine"
}

# install keystone  ---gcc-4.8&&g++-4.8 is OK and gcc-4.6||g++-4.6 is awful:(
function keystone {
	sudo apt-get install cmake
	check_result "install CMake for keystone-engine"
	git clone https://github.com/keystone-engine/keystone.git
	# if failed when compiling , after meeting with all the dependency , it's best to remove the project and git clone it again to compile
	mkdir -p keystone/build
	cd keystone/build && ../make-share.sh && sudo make install && sudo ldconfig && cd ../bindings/python && sudo make install && sudo make install3
	check_result "install keystone-engine"
	cd ../../..
}

# install unicorn
function unicorn {
	sudo apt-get install libglib2.0-dev
	check_result "install libglib2.0-dev for unicorn-engine"
	git clone https://github.com/unicorn-engine/unicorn.git
	# if failed when compiling , after meeting with all the dependency , it's best to remove the project and git clone it again to compile
	cd unicorn && ./make.sh gcc && sudo ./make.sh install && cd bindings/python && sudo make install && sudo make install3
	check_result "install unicorn-engine"
	cd ../../..
}

# install ROPGadget
function ROPGadget {
	sudo pip install ropgadget

	sudo pip3 install ropgadget
}
# install gef
function gef {
	wget -q -O- https://github.com/hugsy/gef/raw/master/gef.sh | sh
	check_result "install gef"
}

# setup checksec
function checksec {
    sudo wget https://github.com/slimm609/checksec.sh/raw/master/checksec -O /usr/local/bin/checksec && chmod +x /usr/local/bin/checksec
    check_result "install checksec"
}


if [ -z $1 ]
then
    init
    pwn
    capstone
    keystone
    unicorn
    ROPGadget
    gef
    checksec
else
    for i in $@
    do
        $i
    done
fi
