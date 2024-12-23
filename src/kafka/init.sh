#!/bin/bash

## Zookeeper와 Kafka 브로커의 디렉토리를 생성한다.
mkdir -p /data/zookeeper
mkdir -p /data/kafka-logs

## Zookeeper 서버별로 ID값을 생성한다.
echo 1 | tee /data/zookeeper/myid

## 초기 패키지를 설치한다.
yum -y install java-17-amazon-corretto java-17-amazon-corretto-devel
cd /usr/local/src
wget https://packages.confluent.io/archive/7.7/confluent-community-7.7.0.tar.gz
tar -xvf confluent-community-7.7.0.tar.gz
cp -arp confluent-7.7.0 /usr/local/confluent

cd /usr/local/confluent/etc/kafka


## Kafka 브로커 설정을 변경한다.
mv server.properties server_BAK
cat <<EOF > /usr/local/confluent/etc/kafka/server.properties
############################# Server Basics #############################
broker.id=1
listeners=PLAINTEXT://10.x.x.x:9092
advertised.listeners=PLAINTEXT://10.x.x.x:9092
############################# Log Basics #############################
log.dirs=/data/kafka-logs
num.partitions=3
############################# Internal Topic Settings  #############################
offsets.topic.replication.factor=3
transaction.state.log.replication.factor=3
transaction.state.log.min.isr=3
############################# Zookeeper #############################
zookeeper.connect=10.x.x.x:2181,10.x.x.x:2181,10.x.x.x:2181
EOF

## Zookeeper 설정을 변경한다.
mv zookeeper.properties zookeeper_BAK
cat <<EOF > /usr/local/confluent/etc/kafka/zookeeper.properties
dataDir=/data/zookeeper
clientPort=2181
maxClientCnxns=0
admin.enableServer=false
initLimit=5
syncLimit=2
server.1=10.100.100.222:2888:3888
server.2=10.100.100.174:2888:3888
server.3=10.100.100.197:2888:3888
EOF

## Kafka Home 디렉토리 설정을 profile에 저장한다.
echo "KAFKA_HOME=/usr/local/confluent
export PATH=\$PATH:\$KAFKA_HOME/bin" >> /etc/profile
source /etc/profile

## Zookeeper system daemon File을 생성한다.
cat <<EOF > /usr/lib/systemd/system/zookeeper.service
[Unit]
Description=Apache Zookeeper server
Documentation=http://zookeeper.apache.org
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
ExecStart=/usr/bin/bash /usr/local/confluent/bin/zookeeper-server-start /usr/local/confluent/etc/kafka/zookeeper.properties
ExecStop=/usr/bin/bash /usr/local/confluent/bin/zookeeper-server-stop
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
EOF


## Kafka system daemon File을 생성한다.
cat <<EOF >> /usr/lib/systemd/system/kafka-broker.service
[Unit]
Description=Apache Kafka Server
Documentation=http://kafka.apache.org/documentation.html
Requires=zookeeper.service

[Service]
Type=simple
Environment="JAVA_HOME=/usr/lib/jvm/java-17-amazon-corretto.x86_64"
ExecStart=/usr/bin/bash /usr/local/confluent/bin/kafka-server-start /usr/local/confluent/etc/kafka/server.properties
ExecStop=/usr/bin/bash /usr/local/confluent/bin/kafka-server-stop

[Install]
WantedBy=multi-user.target
EOF

## Systemd Reload
systemctl daemon-reload
systemctl enable --now zookeeper.servie kafka-broker.service