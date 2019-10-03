Installation guide
******************
System requirements
===================
One of the unique features of the ``reg_utils`` package is that ``reg_interface`` 
part of it can work both on the host PC and on the ARM co-CPU of the backend electronics like Zynq. 

Certain packages depending on the architecture has to be installed on the system. They are listed below.

ARM(Zynq) installation
----------------------
The RPM provided is compiled for hard float architecture. You will need a corresponding peta-linux distributive containing the following packages:

* `python2.7`
* 

TODOHost PC installation
------------------------
You need to have following software installed:

* `python2.7` or above
* `libwiscrpcsvc`
* `liblog4cplus` of version 1.2.5  which can be installed standalone or as part of the `xdaq` distribuion
* TODO - complete after librwreg migration

The packaging tools provide `rpm` and `pip`-installable packages. 
To install with `pip` system-wide:

>>> pip install reg_utils-X.Y.Z.tar.gz

You need to have `sudo` privileges to do so.

If you need to install the package locally, you can do it running 

>>> pip --user install reg_utils-X.Y.Z.tar.gz

and the package will be installed under ``~/.local/lib/``


