# TODO

## Links

  * https://andy-carter.com/blog/setting-up-travis-locally-with-docker-to-test-continuous-integration
  * https://gist.github.com/fulldecent/d84cd1abdcc6930865d1b862c4aed917
  * https://bl.ocks.org/purp/0df77b579031127f10f31ebd202e8fd4
  * https://quay.io/repository/travisci/ci-python?tab=tags
  * https://hub.docker.com/r/travisci/ci-python/tags - this seems to be more recent

## Installing docker

Installing under ubuntu
```
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt install docker
sudo usermod -aG docker richard
```

To test
```
docker run hello-world
```

## Running travis locally

### Create docker container

First lets pull the latest docker image for travis python
```
docker pull travisci/ci-python:packer-1490914243
```

Next lets startup a container in the background
```
docker run --name travis-debug -dit travisci/ci-python:packer-1490914243 /sbin/init
```

### Connect to the docker container

Connect to the docker running container
```
docker exec -it travis-debug bash -l
```

Switch to the travis user
```
su - travis
```

### Setup container for build

Next we need to clone the travis build repo
```
cd ~/builds
git clone https://github.com/travis-ci/travis-build.git
cd travis-build

gem install travis
travis
bundle install
#bundler add travis
bundler binstubs travis
ln -s `pwd` ~/.travis/travis-build
```

cd ~/builds
git clone https://github.com/Hecatron/py-makefile-dbparse.git
cd py-makefile-dbparse

travis compile > ci.sh


TODO
gem install bundler


Update ruby version manager
```
gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
rvm get stable
```

rvm upgrade 2.3.0



### Clean up old container

To stop and remove the container
```
docker stop travis-debug
docker rm travis-debug
```








docker pull quay.io/travisci/travis-python
docker pull quay.io/travisci/ci-python:packer-1475058170




```
# Setup a docker image
docker run -it -u travis quay.io/travisci/travis-python /bin/bash

docker run --name travis-debug -dit quay.io/travisci/ci-python /sbin/init



# Install a recent ruby (default is 1.9.3)
rvm install 2.3.0
rvm use 2.3.0

# Install travis-build to generate a .sh out of .travis.yml
cd ~/builds
git clone https://github.com/travis-ci/travis-build.git
cd travis-build

gem install travis
travis # to create ~/.travis \
ln -s `pwd` ~/.travis/travis-build \
bundle install

```


try this:
rvm install 2.4.9
rvm use 2.4.9




rvm get stable
