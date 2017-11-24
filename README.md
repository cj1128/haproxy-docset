# HAProxy docset for dash

take following steps to generate haproxy docset.

1. download html page

```bash
wget -E -H -k -p http://cbonte.github.io/haproxy-dconv/1.7/configuration.html
```

2. modify html page, remove header and sidebar, adjust some styles

## Reference

- [Docset Generation Guide](https://kapeli.com/docsets#dashDocset)
