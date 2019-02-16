---
layout: post
title:  "Building pyrocksdb on ubuntu"
date: 2019-02-16 01:30:00
categories: python open-source databases
description: How to build pyrocksdb with python
published: true
---

The latest versions of pyrocksdb does not build on ubuntu.

It seems the library is not compatible with the latest versions of rocksdb.

First, install dependency libraries:

```bash
apt-get install build-essential libsnappy-dev zlib1g-dev libbz2-dev \
    libgflags-dev liblz4-dev libzstd-dev git-core -y
```


Then, checkout a tag of the 4.x line of rocksdb:

```bash
git clone https://github.com/facebook/rocksdb.git --branch=v4.13.5 /usr/src/rocksdb
```

And finally, build the library:

```bash
cd /usr/src/rocksdb
make shared_lib
make install-shared INSTALL_PATH=/usr
```


Finally, install pyrocksdb with pip:

```bash
pip install Cython
pip install python-rocksdb
```