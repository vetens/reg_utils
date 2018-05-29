SUBPACKAGES := \
        python

DOC := \
	doc

SUBPACKAGES.DEBUG    := $(patsubst %,%.debug,    ${SUBPACKAGES})
SUBPACKAGES.RPM      := $(patsubst %,%.rpm,      ${SUBPACKAGES})
SUBPACKAGES.CLEANRPM := $(patsubst %,%.cleanrpm, ${SUBPACKAGES})
SUBPACKAGES.CLEAN    := $(patsubst %,%.clean,    ${SUBPACKAGES})

DOC.CLEAN := $(patsubst %,%.clean, ${DOC})

.PHONY: doc

all: $(SUBPACKAGES) $(SUBPACKAGES.RPM) $(DOC)

rpm: $(SUBPACKAGES) $(SUBPACKAGES.RPM)

cleanrpm: $(SUBPACKAGES.CLEANRPM)

clean: $(SUBPACKAGES.CLEAN) $(DOC.CLEAN)

$(DOC):
	$(MAKE) -C $@ html

$(SUBPACKAGES):
	$(MAKE) -C $@

$(SUBPACKAGES.RPM):
	$(MAKE) -C $(patsubst %.rpm,%, $@) rpm

$(SUBPACKAGES.CLEANRPM):
	$(MAKE) -C $(patsubst %.cleanrpm,%, $@) cleanrpm

$(SUBPACKAGES.CLEAN):
	$(MAKE) -C $(patsubst %.clean,%, $@) clean

$(DOC.CLEAN):
	$(MAKE) -C $(patsubst %.clean,%, $@) clean
