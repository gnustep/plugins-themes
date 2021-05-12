
ifeq ($(GNUSTEP_MAKEFILES),)
 GNUSTEP_MAKEFILES := $(shell gnustep-config --variable=GNUSTEP_MAKEFILES 2>/dev/null)
  ifeq ($(GNUSTEP_MAKEFILES),)
    $(warning )
    $(warning Unable to obtain GNUSTEP_MAKEFILES setting from gnustep-config!)
    $(warning Perhaps gnustep-make is not properly installed,)
    $(warning so gnustep-config is not in your PATH.)
    $(warning )
    $(warning Your PATH is currently $(PATH))
    $(warning )
  endif
endif

ifeq ($(GNUSTEP_MAKEFILES),)
  $(error You need to set GNUSTEP_MAKEFILES before compiling!)
endif

# GNUstep Themes

PACKAGE_NAME = GNUstepThemes
include $(GNUSTEP_MAKEFILES)/common.make

#
# Themes resources
# 
RESOURCE_SET_NAME = Themes
Themes_INSTALL_DIR = $(GNUSTEP_LIBRARY)/Themes
Themes_RESOURCE_FILES = Darkness.themes

include $(GNUSTEP_MAKEFILES)/resource-set.make
