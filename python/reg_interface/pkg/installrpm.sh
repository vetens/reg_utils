#!/bin/sh

# default action
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

# install 'scripts' to /opt/reg_utils/bin
mkdir -p %{buildroot}/opt/reg_utils/bin
cp -rfp reg_utils/scripts/*.py %{buildroot}/opt/reg_utils/bin/

find %{buildroot} -type f -exec chmod a+r {} \;
find %{buildroot} -type f -iname '*.cfg' -exec chmod a-x {} \;

# set permissions
cat <<EOF >>INSTALLED_FILES
%attr(0755,root,root) /opt/reg_utils/bin/*.py
%attr(0755,root,root) /usr/lib/python*/site-packages/reg_utils/scripts/*.py
EOF
echo "Modified INSTALLED_FILES"
cat INSTALLED_FILES
