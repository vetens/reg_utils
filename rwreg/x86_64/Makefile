WISC_RPCSVC  := /opt/wiscrpcsvc
BUILD_HOME   := $(shell dirname `cd ../../; pwd`)
Project      := reg_utils
Package      := rwreg
ShortPackage := rwreg
LongPackage  := rwreg
PackageName  := $(ShortPackage)
PackagePath  := $(shell pwd)
PackageDir   := pkg/$(ShortPackage)
Arch         := x86_64
Packager     := Mykhailo Dalchenko
REG_UTILS    := $(BUILD_HOME)/reg_utils

RWREG_VER_MAJOR:=$(shell $(BUILD_HOME)/$(Project)/config/tag2rel.sh | awk '{split($$0,a," "); print a[1];}' | awk '{split($$0,b,":"); print b[2];}')
RWREG_VER_MINOR:=$(shell $(BUILD_HOME)/$(Project)/config/tag2rel.sh | awk '{split($$0,a," "); print a[2];}' | awk '{split($$0,b,":"); print b[2];}')
RWREG_VER_PATCH:=$(shell $(BUILD_HOME)/$(Project)/config/tag2rel.sh | awk '{split($$0,a," "); print a[3];}' | awk '{split($$0,b,":"); print b[2];}')

include $(BUILD_HOME)/$(Project)/config/mfCommonDefs.mk
include $(BUILD_HOME)/$(Project)/config/mfRPMRules.mk

CCFLAGS=-O0 -g3 -fno-inline -Wall -fPIC -pthread -m64

LDFLAGS=-shared

IncludeDirs= ${BUILD_HOME}/${Project}/${Package}/${Arch}/include
INC=$(IncludeDirs:%=-I%)

Libraries= -lwiscrpcsvc
#assume wiscrpcsvc installed system-wide. Not sure how to fix in docker

LIB = -L${WISC_RPCSVC}/lib
LIB += $(Libraries)

SRCS_RPC_SA = $(shell echo src/*.cc)
OBJS_RPC_SA = $(SRCS_RPC_SA:.cc=.o)

RPC_SA_LIB=${BUILD_HOME}/${Project}/${Package}/${Arch}/lib/librwreg.so

.PHONY: clean rpc prerpm doc

default:
	@echo "Running default target"
	$(MakeDir) $(PackageDir)

_rpmprep: preprpm
	@echo "Running _rpmprep target"
preprpm: default
	@echo "Running preprpm target"
	@cp -rf lib $(PackageDir)

build: rpc

_all:${RPC_SA_LIB} 

rpc:${RPC_SA_LIB}

$(RPC_SA_LIB): $(OBJS_RPC_SA)
	@mkdir -p ${BUILD_HOME}/${Project}/${Package}/${Arch}/lib/
	$(CC) $(CCFLAGS) $(LDFLAGS) $(INC) $(LIB) -o $@ $^

$(OBJS_RPC_SA):$(SRCS_RPC_SA)
	$(CC) $(CCFLAGS) $(INC) -c -o $@ $<

doc:
clean: cleanrpm
	-${RM} ${RPC_SA_LIB} ${OBJS_RPC_SA} 
	-rm -rf $(PackageDir)

cleandoc: 
	-rm-rf doc/html  doc/latex  doc/xml
