jdoc
====

A pydoc-like tool for interacting with Javadoc 

(Because I gave up IntelliJ for Lent)

_Warning: In a very hacky state and under development_

Usage
-----

```
./bin/jdoc -h
```

Examples
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

Or regular expression

```
./bin/jdoc 'com.(airbnb|google)'
```

Show plaintext Javadoc for a class (note: need to narrow down parameters to get one match)

```
./bin/jdoc org.apache.http.client.HttpClient
```

Or dump the source

```
./bin/jdoc org.apache.http.client.HttpClient --show_source
```
