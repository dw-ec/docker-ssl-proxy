# Docker-compose project demonstrating docker-ssl-proxy

The purpose of this demonstration is to show multiple containers all using the
same shared SSL CA (certificate authority), and being able to make HTTPS
connections to one another without any errors about untrusted certificates.

See [docker-compose.yml](./docker-compose.yml) for details.

## Web services

There are 2 simple python-flask web services with the following functions:

- hello_service: Says "Hello world!" on http://hello.demo/

- clock_service: Returns the current time when you visit any valid subdomain 
and city e.g: http://america.clock.demo/los_angeles 

## Docker-ssl-proxy services

Each web service has its own docker-ssl-proxy container for fielding https
requests:

- hello_proxy

- clock_proxy

## HTTPS requests between containers

To demonstrate SSL certificate trust between containers, the hello_service has
a special hidden feature whereby you can query a continent & city. It will
then make an API call to the clock_service container over HTTPS, retrieving the
output and delivering it in its payload back to your browser.

E.g:

- https://asia.clock.demo/shanghai - direct query to the clock_service

- https://hello.demo/time/asia/shanghai - indirect query via hello_service

## Trying out the demo

```
# docker-compose build

# docker-compose up
```

### Configuring Linux workstation so you can browse the services

You can browse the demo services in your browser if you add the dns_proxy
container to your system's DNS resolvers list, and if you install the CA
certificate into your system's trusted key store.

#### Ubuntu and similar systemd-based distros
Edit /etc/systemd/resolved.conf and set the "DNS" line to be something like:
```
DNS=192.168.69.53 8.8.8.8 8.8.4.4
```
Then restart resolved:
```
sudo systemctl restart systemd-resolved
```

Trust the CA cert with:
```
sudo cp https-proxy-ca/rootCA.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

#### Traditional linux / unix systems
Just add the dns_proxy container's IP above the existing entries in
/etc/resolv.conf:
```
nameserver 192.168.69.53
```

Every distro seems to have its own way of installing a CA certificate so that's
an exercise for the user.


### Configuring a Mac OSX workstation so you can browse the services

Docker for Mac doesn't give you network access to your docker environment. I.e.
it's very broken. To browse your containers you'll need to essentially VPN in
to your Docker environment: https://github.com/wojas/docker-mac-network

Follow those instructions and once it's spat out the docker-for-mac.ovpn file,
before importing it into tunnelblick append the following lines to the bottom:

```
route 192.168.69.0 255.255.255.0
dhcp-option DNS 192.168.69.53
dhcp-option DNS 8.8.8.8
dhcp-option DNS 8.8.4.4
comp-lzo no
```

Once imported, you may need to set `☑️ Allow changes to manually-set network settings`
within tunnelblick's UI.
Connect to the Docker internal network VPN and you should now be able to browse the
demo container urls like https://hello.demo/

To trust the project's CA certificate, just do:
```
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain https-proxy-ca/rootCA.crt
```
