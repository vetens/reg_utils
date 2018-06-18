ifndef PETA_STAGE
$(error "Error: PETA_STAGE environment variable not set.  Change to the root of your PetaLinux install, and source the settings.sh file")
endif

BUILD_HOME   := $(shell dirname `cd ../../; pwd`)
Project      := reg_utils
Package      := rwreg
ShortPackage := rwreg
LongPackage  := rwreg
PackageName  := $(ShortPackage)
PackagePath  := $(shell pwd)
PackageDir   := pkg/$(ShortPackage)
Arch         := arm
Packager     := Mykhailo Dalchenko

RWREG_VER_MAJOR=1
RWREG_VER_MINOR=0
RWREG_VER_PATCH=0

include $(BUILD_HOME)/$(Project)/config/mfZynq.mk
include $(BUILD_HOME)/$(Project)/config/mfCommonDefs.mk
include $(BUILD_HOME)/$(Project)/config/mfRPMRules.mk

IncludeDirs= ${BUILD_HOME}/${Project}/${Package}/${Arch}/include
INC=$(IncludeDirs:%=-I%)

LIB_ARM_RWREG_OBJS=src/libmemsvc.o src/rwreg.o
LIB_ARM_RWREG=${BUILD_HOME}/${Project}/${Package}/${Arch}/lib/librwreg.so

.PHONY: clean rpc prerpm

default:
	@echo "Running default target"
	$(MakeDir) $(PackageDir)

_rpmprep: preprpm
	@echo "Running _rpmprep target"
preprpm: default
	@echo "Running preprpm target"
	@cp -rf lib $(PackageDir)

build: $(LIB_ARM_RWREG)

_all: $(LIB_ARM_RWREG)

$(LIB_ARM_RWREG):$(LIB_ARM_RWREG_OBJS)
	@mkdir -p ${BUILD_HOME}/${Project}/${Package}/${Arch}/lib/
	$(CXX) -std=c++0x $(LDFLAGS) $(INC) -fnon-call-exceptions -shared -o $@ $(LIB_ARM_RWREG_OBJS) 

%.o: %.c
	$(CC) -std=gnu99 -c $(CFLAGS) $(INC) -o $@ $<
%.o: %.cc
	$(CXX) -std=c++0x -c $(CFLAGS) $(INC) -o $@ $<

clean: cleanrpm
	-${RM} ${LIB_ARM_RWREG} ${LIB_ARM_RWREG_OBJS}
	-rm -rf $(PackageDir)

cleandoc: 
	@echo "TO DO"
