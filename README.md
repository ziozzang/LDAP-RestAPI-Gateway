# LDAP-RestfulAPI-Server

# TL; DR
Generic LDAP Server does't support RESTful API.
This is for Generic LDAP Gateway Server to support REST API Server for LDAP.

# Author
Jioh L. Jung

# How to use.
* Fix Configuration file.
* Build Dockerfile to use server. :)
* Run docker with option :)

```
docker build -t ldap-gateway .
docker run -d --name gateway \
  -v `pwd`/src/conf.py:/opt/conf.py \
  -p 5000:5000 ldap-gateway
```

# Copyright
MIT Licese
* If you need to fix code, Just do it :)

# Docs
* Check docs folder. :D 
