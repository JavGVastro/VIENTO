#!/bin/bash

folders=(
    "r150pc-HI-6563"
    "r50pc-HI-6563"
    #"r100pc-OIII-5007"
    #"r100pc-SII-6731"
    #"r100pc-SIII-9069"
)

for dir in "${folders[@]}"; do
    echo "Running: $dir"
    cd "$dir" || exit 1
    make -f Makefile_pipeline_list all || exit 1
    cd ..
done
