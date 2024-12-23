#!/bin/bash
## InfluxDB 레포지토리를 추가한다.
cat <<EOF | sudo tee /etc/yum.repos.d/influxdata.repo
[influxdata]
name = InfluxData Repository - Stable
baseurl = https://repos.influxdata.com/stable/\$basearch/main
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdata-archive_compat.key
EOF

## InfluxDB를 설치한다.
yum install influxdb2 influxdb2-cli

## 추가스토리지를 설정한다.
mkdir /data
fdisk /dev/xvdb
mkfs.xfs /dev/xvdb1
mount /dev/xvdb1 /data
echo "UUID=$(blkid -s UUID -o value /dev/xvdb1)     /data   xfs     defaults        0       0" >> /etc/fstab

chown -R influxdb:influxdb /data
mv /var/lib/influxdb/* /data

## InfluxDB 설정을 변경한다.
mv /etc/influxdb/config.toml /etc/influxdb/config_BAK
cat <<EOF > /etc/influxdb/config.toml
bolt-path = "/data/influxd.bolt"
engine-path = "/data/engine"
EOF

## Systemd 등록
systemctl enable --now influxdb