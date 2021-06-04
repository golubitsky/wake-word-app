#!/usr/bin/env bash

# Followed https://github.com/bbc/audiowaveform/issues/27
# Might not be necessary if we use conda install instead of pip install?
# We faced the same 'null' error after installing manually as after conda install -- we resolved
# that error by writing the bytes to a file before reading that file using librosa.
wget https://github.com/libsndfile/libsndfile/releases/download/1.0.31/libsndfile-1.0.31.tar.bz2
tar -xf libsndfile-1.0.31.tar.bz2
cd libsndfile-1.0.31
./configure --prefix=/usr --disable-static --docdir=/usr/share/doc/libsndfile-1.0.31
make
sudo make install
