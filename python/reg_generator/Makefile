#
# Makefile for vfatqc package
#

BUILD_HOME := $(shell dirname `cd ../../; pwd`)

Project      := reg_utils
ShortProject := reg_utils
Namespace    := reg_utils
Package      := reg_generator
ShortPackage := reg_generator
LongPackage  := reg_generator
PackageName  := $(ShortPackage)
PackagePath  := $(shell pwd)
PackageDir   := pkg/$(Namespace)/$(ShortPackage)
ScriptDir    := pkg/$(Namespace)/scripts


# Explicitly define the modules that are being exported (for PEP420 compliance)
PythonModules = ["$(Namespace).$(ShortPackage)"]
$(info PythonModules=${PythonModules})

REG_GENERATOR_VER_MAJOR=1
REG_GENERATOR_VER_MINOR=0
REG_GENERATOR_VER_PATCH=0

include $(BUILD_HOME)/$(Project)/config/mfCommonDefs.mk
include $(BUILD_HOME)/$(Project)/config/mfPythonDefs.mk

# include $(BUILD_HOME)/$(Project)/config/mfDefs.mk

include $(BUILD_HOME)/$(Project)/config/mfPythonRPM.mk

default:
	@echo "Running default target"
	$(MakeDir) $(PackageDir)
	@echo "__path__ = __import__('pkgutil').extend_path(__path__, __name__)" > pkg/$(Namespace)/__init__.py
	# @cp -rf __init__.py $(PackageDir)

# need to ensure that the python only stuff is packaged into RPMs
.PHONY: clean preprpm
_rpmprep: preprpm
	@echo "Running _rpmprep target"
preprpm: default
	@echo "Running preprpm target"
	$(MakeDir) $(ScriptDir)
	@cp -rf generate_registers.py $(ScriptDir)
	@cp -rf generate_registers.py $(PackageDir)
	-cp -rf README.md LICENSE CHANGELOG.md MANIFEST.in requirements.txt $(PackageDir)
	-cp -rf README.md LICENSE CHANGELOG.md MANIFEST.in requirements.txt pkg

clean:
	@echo "Running clean target"
	-rm -rf $(ScriptDir)
	-rm -rf $(PackageDir)
	-rm -f  pkg/$(Namespace)/__init__.py
	-rm -f  pkg/README.md
	-rm -f  pkg/LICENSE
	-rm -f  pkg/MANIFEST.in
	-rm -f  pkg/CHANGELOG.md
	-rm -f  pkg/requirements.txt

print-env:
	@echo BUILD_HOME     $(BUILD_HOME)
	@echo PackagePath    $(PackagePath)
	@echo GIT_VERSION    $(GIT_VERSION)
	@echo PYTHON_VERSION $(PYTHON_VERSION)
	@echo GEMDEVELOPER   $(GEMDEVELOPER)
