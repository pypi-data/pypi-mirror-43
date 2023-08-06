# Aliyun DNS plugin for autocert project

This plugin provides an automated `perform_dns01()` for
[autocert](https://github.com/Smart-Hypercube/autocert/tree/master/letsencrypt#apply-for-some-certificates).

```python3
# other kinds of credential, e.g. StsTokenCredential, can be used as well
credential = AccessKeyCredential(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
with AliyunDNS(credential) as aliyun:
    result = le.order(k2, domains, aliyun.perform_dns01)
# added DNS records will be removed automatically
```
