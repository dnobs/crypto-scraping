#!/bin/sh
source /opt/anaconda3/etc/profile.d/conda.sh

echo packaging conda environment
conda activate env_crypto-rnn
conda env export -f env_crypto-scraping.yml --no-builds
