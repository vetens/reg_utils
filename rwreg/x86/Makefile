WISC_RPCSVC  := /opt/wiscrpcsvc
BUILD_HOME   := $(shell dirname `cd ../../; pwd`)
Project      := reg_utils
Package      := rwreg
ShortPackage := rwreg
LongPackage  := rwreg
PackageName  := $(ShortPackage)
PackagePath  := $(shell pwd)
PackageDir   := pkg/$(ShortPackage)
Arch         := x86

RWREG_VER_MAJOR=1
RWREG_VER_MINOR=0
RWREG_VER_PATCH=0

#include $(BUILD_HOME)/$(Project)/config/mfCommonDefs.mk
#include $(BUILD_HOME)/$(Project)/config/mfDefsGEM.mk

CC=g++
CCFLAGS=-O0 -g3 -fno-inline -Wall -fPIC -pthread -m64
ADDFLAGS=-std=gnu++14

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

.PHONY: clean

all:${RPC_SA_LIB} 

rpc:${RPC_SA_LIB}

$(RPC_SA_LIB): $(OBJS_RPC_SA)
	@mkdir -p ${BUILD_HOME}/${Project}/${Package}/${Arch}/lib/
	$(CC) $(CCFLAGS) $(ADDFLAGS) $(LDFLAGS) $(INC) $(LIB) -o $@ $^

$(OBJS_RPC_SA):$(SRCS_RPC_SA)
	$(CC) $(CCFLAGS) $(ADDFLAGS) $(INC) -c -o $@ $<


clean:
	-${RM} ${RPC_SA_LIB} ${OBJS_RPC_SA}
