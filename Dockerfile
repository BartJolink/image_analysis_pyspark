FROM node:12.16.3

USER root
WORKDIR /

RUN apt-get update && apt-get -y install \
    python3 \
    python3-pip \
    openjdk-8-jdk \
    wget \
    nano \
    ssh \
    rsync \
    vim

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir nibabel pydicom matplotlib pillow && \
    pip3 install --no-cache-dir med2image

RUN pip3 install pyspark

RUN \
  ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
  chmod 0600 ~/.ssh/authorized_keys

RUN wget http://apache.mirrors.tds.net/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz && \
    tar -xzf hadoop-3.3.0.tar.gz && \
    rm -rf /hadoop-3.3.0.tar.gz
ENV hadoop="/hadoop/"


ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

ENV HDFS_NAMENODE_USER "root"
ENV HDFS_DATANODE_USER "root"
ENV HDFS_SECONDARYNAMENODE_USER "root"
ENV YARN_RESOURCEMANAGER_USER "root"
ENV YARN_NODEMANAGER_USER "root"

RUN echo "export JAVA_HOME=$JAVA_HOME" >> /hadoop-3.3.0/etc/hadoop/hadoop-env.sh && \
    echo "PATH=$PATH:/hadoop-3.3.0/bin" >> ~/.bashrc

SHELL ["/bin/bash", "-c"]

ADD ./ /image_analysis

WORKDIR /image_analysis