#!/bin/sh -e

# Wait for CA cert to exist
while [ ! -s /etc/ssl/shared-ca/rootCA.crt ] ; do
  echo "waiting for CA cert to exist"
  sleep 1
done

# Install CA certificate
echo "installing CA cert"
cp /etc/ssl/shared-ca/rootCA.crt /usr/local/share/ca-certificates/
update-ca-certificates

# Start service
echo "Starting clock service"
python -u ./clock-server.py

