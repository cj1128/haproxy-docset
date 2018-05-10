# HAProxy Dash Docset

## Build

1. Download html pages

    ```bash
    wget -E -H -k -p http://cbonte.github.io/haproxy-dconv/1.7/configuration.html
    wget -E -H -k -p http://cbonte.github.io/haproxy-dconv/1.7/management.html
    ```

2. Modify html pages, remove header and sidebar, adjust some styles

3. Build index

    ```bash
    ./build.py [version]
    ```

4. Add to dash

    open Dash -> Preferences -> Docsets, click `+`, select target docset file in `dist` dir.

## Reference

- [Docset Generation Guide](https://kapeli.com/docsets#dashDocset)
