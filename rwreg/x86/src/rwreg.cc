#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "wiscrpcsvc.h"

#define DLLEXPORT extern "C"

#define STANDARD_CATCH \
	catch (wisc::RPCSvc::NotConnectedException &e) { \
		printf("Caught NotConnectedException: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCSvc::RPCErrorException &e) { \
		printf("Caught RPCErrorException: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCSvc::RPCException &e) { \
		printf("Caught exception: %s\n", e.message.c_str()); \
		return 1; \
	} \
	catch (wisc::RPCMsg::BadKeyException &e) { \
		printf("Caught exception: %s\n", e.key.c_str()); \
		return 0xdeaddead; \
	} 

#define ASSERT(x) do { \
		if (!(x)) { \
			printf("Assertion Failed on line %u: %s\n", __LINE__, #x); \
			return 1; \
		} \
	} while (0)

static wisc::RPCSvc rpc;
static wisc::RPCMsg req, rsp;

DLLEXPORT uint32_t init(char * hostname)
{
  try {
		rpc.connect(hostname);
	}
	catch (wisc::RPCSvc::ConnectionFailedException &e) {
		printf("Caught RPCErrorException: %s\n", e.message.c_str());
		return 1;
	}
	catch (wisc::RPCSvc::RPCException &e) {
		printf("Caught exception: %s\n", e.message.c_str());
		return 1;
	}

  try {
  		ASSERT(rpc.load_module("memory", "memory v1.0.1"));
  		ASSERT(rpc.load_module("extras", "extras v1.0.1"));
  		ASSERT(rpc.load_module("utils", "utils v1.0.1"));
  		ASSERT(rpc.load_module("optohybrid", "optohybrid v1.0.1"));
  		ASSERT(rpc.load_module("amc", "amc v1.0.1"));
  		ASSERT(rpc.load_module("calibration_routines", "calibration_routines v1.0.1"));
  	}
  	STANDARD_CATCH;

  return 0;
}

DLLEXPORT unsigned long getReg(unsigned int address)
{
	req = wisc::RPCMsg("memory.read");
	req.set_word("address", address);
	req.set_word("count", 1);
	try {
		rsp = rpc.call_method(req);
	}
	STANDARD_CATCH;

	uint32_t result;
  try{
	  if (rsp.get_key_exists("error")) {
      return 0xdeaddead;
    } else {
	    ASSERT(rsp.get_word_array_size("data") == 1);
      rsp.get_word_array("data", &result);
    }
  }
	STANDARD_CATCH;

	return result;
}

DLLEXPORT unsigned long getBlock(unsigned int address, uint32_t* result, ssize_t size)
{
 	req = wisc::RPCMsg("extras.blockread");
	req.set_word("address", address);
	req.set_word("count", size);
	try {
		rsp = rpc.call_method(req);
	}
	STANDARD_CATCH;

  try{
	  if (rsp.get_key_exists("error")) {
      return 1;
    } else {
	    ASSERT(rsp.get_word_array_size("data") == size);
      rsp.get_word_array("data", result);
    }
  }
	STANDARD_CATCH;
  return 0;
}

DLLEXPORT unsigned long getList(uint32_t* addresses, uint32_t* result, ssize_t size)
{
 	req = wisc::RPCMsg("extras.listread");
	req.set_word_array("addresses", addresses,size);
	req.set_word("count", size);
	try {
		rsp = rpc.call_method(req);
	}
	STANDARD_CATCH;

  try{
	  if (rsp.get_key_exists("error")) {
      return 1;
    } else {
	    ASSERT(rsp.get_word_array_size("data") == size);
      rsp.get_word_array("data", result);
    }
  }
	STANDARD_CATCH;
  return 0;
}
DLLEXPORT unsigned long putReg(unsigned int address, unsigned int value)
{
	req = wisc::RPCMsg("memory.write");
	req.set_word("address", address);
	req.set_word_array("data", &value,1);
	try {
		rsp = rpc.call_method(req);
	}
	STANDARD_CATCH;
  if (rsp.get_key_exists("error")) {
    return 0xdeaddead;
  } else return value;
}
