#!/bin/bash
# TODO(greg_brandt) Use nosetests or something

./bin/jdoc org.apache
./bin/jdoc --group org.apache.httpcomponents --artifact httpclient --version 4.5.3
./bin/jdoc 'com.(airbnb|google)'
./bin/jdoc -c HttpClient
./bin/jdoc org.apache.http.client.HttpClient
./bin/jdoc org.apache.http.client.HttpClient --show_source
