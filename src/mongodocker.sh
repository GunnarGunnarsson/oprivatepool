#!/bin/bash

DATA_DIR=~/.rideshare_mongo/

mkdir -p "$DATA_DIR"
chmod 777 "$DATA_DIR"

OPTS="-d -p 27017:27017 --name ridemongodb"

case "$OSTYPE" in
    darwin*)
        # Assumes there's a default docker machine
        docker-machine start default
        eval "$(docker-machine env default)"
    ;; 
    msys*)
        # Assumes there's a default docker machine
        # Untested on windows
        docker-machine start default
        eval "$(docker-machine env default)"
    ;;
    # solaris*) echo "SOLARIS" ;;
    linux*)
        # On linux we can persist the data. All other systems needs to recreate the data upon reboot.
        OPTS="$OPTS -v $DATA_DIR:/data/db"
    ;;
    # bsd*)     echo "BSD" ;;
    *)      
    ;; # echo "unknown: $OSTYPE" ;;
esac

docker run $OPTS mongo
