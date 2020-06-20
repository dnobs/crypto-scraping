#!/bin/sh

#################
# GIT STUFF
# install git
read -p "Enter Github pw: "  gitpw


# clone github repo
git clone
#################


#################
# CONDA STUFF
# install conda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod 755 Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh

# respond to prompts
# restart command window

# create conda env based on saved yml file
conda env create -f=env_crypto-scraping.yml
conda activate env_crypto-scraping

# activate conda env
source /opt/anaconda3/etc/profile.d/conda.sh
#################

# run helloworld python file
