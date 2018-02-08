if [[ ! "$0" =~ ("bash") ]]
then
    # best for calling from zsh                                                                                                                                                                                                                                                   
    export REG_UTILS=$(dirname $(readlink -f "$0") )
else
    # bash specific, must be sourced from a bash shell...                                                                                                                                                                                                                         
    export REG_UTILS=$(dirname $(readlink -f "${BASH_SOURCE[0]}"))
fi

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$REG_UTILS/lib
export PATH=$PATH:$REG_UTILS/python/reg_interface
