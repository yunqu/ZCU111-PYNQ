LOCAL_SRC := $(wildcard src/*.c)
LIB_NAME := libxrfclk.so
PKG_DIR := xrfclk

all:
	gcc -o $(LIB_NAME) -shared -fPIC -Isrc $(LOCAL_SRC) -DBOARD_${BOARD} -ggdb

install:
	cp $(LIB_NAME) $(PKG_DIR)/
	pip3 install .

clean:
	rm $(LIB_NAME)
