#!/bin/bash -e

# download
[ ! -f SOURCES/Python-2.7.11.tgz ] && curl -o SOURCES/Python-2.7.11.tgz https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz

rpmbuild --define "_topdir `pwd`" --define "_source_filedigest_algorithm md5" --define "_binary_filedigest_algorithm md5" -bs SPECS/python27.spec

mock -r epel-7-x86_64 SRPMS/python27-2.7.11-*.src.rpm
mock -r epel-6-x86_64 SRPMS/python27-2.7.11-*.src.rpm
mock -r epel-5-x86_64 SRPMS/python27-2.7.11-*.src.rpm
