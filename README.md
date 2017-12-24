HTTP Router for simple web application
======================================

How to use
----------

### build and run

```sh
$ ./build.sh
$ python3 ./router.py
```

Access ```http://<router>:8080/config``` and configure.

Access ```http://<router>:8080/route/<target host>/<path>```
will get ```http://<target host>/<path>``` from ```<router>```.

License
-------
MIT License Copyright(c) 2017 Hiroshi Shimamoto
