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

RWREG_VER_MAJOR=1
RWREG_VER_MINOR=0
RWREG_VER_PATCH=0

include $(BUILD_HOME)/$(Project)/config/mfZynq.mk
include $(BUILD_HOME)/$(Project)/config/mfCommonDefs.mk

APP_OBJS=src/libmemsvc.o src/rwreg.o
APP=./lib/librwreg

all: build 

build: $(APP)

$(APP):$(APP_OBJS)
	$(CXX) -std=c++0x $(LDFLAGS) -fnon-call-exceptions -shared -o $@.so $(APP_OBJS) 

%.o: %.c
	$(CC) -std=gnu99 -c $(CFLAGS) -o $@ $<
%.o: %.cc
	$(CXX) -std=c++0x -c $(CFLAGS) -o $@ $<

clean:
	rm -rf lib/*.so lib/*.so.* src/*.o
