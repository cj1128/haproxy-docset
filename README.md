# HAProxy docset for dash

take following steps to generate haproxy docset.

1. download html pages

```bash
wget -E -H -k -p http://cbonte.github.io/haproxy-dconv/1.7/configuration.html
wget -E -H -k -p http://cbonte.github.io/haproxy-dconv/1.7/management.html
```

2. modify html pages, remove header and sidebar, adjust some styles

3. build index

```bash
./build.py [version]
```

4. add to dash

open Dash -> Preferences -> Docsets, click `+`, select target docset file in `dist` dir.

## Reference

- [Docset Generation Guide](https://kapeli.com/docsets#dashDocset)
