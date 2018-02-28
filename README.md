jdoc
====

A pydoc-like tool for interacting with Javadoc (because I gave up IntelliJ for Lent).

_Warning: In a very hacky state and under development_

Usage
-----

Index all documents in local maven repo

```
./bin/jdoc --index
```

Run simple HTTP file server

```
./bin/jdoc --server
```

List classes matching a prefix pattern

```
./bin/jdoc org.apache
```

Or according to certain [Maven Coordinates](https://maven.apache.org/pom.html#Maven_Coordinates)

```
./bin/jdoc --group org.apache.httpcomponents --artifact httpclient --version 4.5.3
```

Show plaintext Javadoc for a class

```
./bin/jdoc org.apache.http.client.HttpClient
```
