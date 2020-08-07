LOCAL_SRC := $(wildcard src/*.c)
TEST_SRC := $(wildcard test/*.c)
LIB_NAME := libxrfclk.so
TEST_EXE := test.elf
PKG_DIR := xrfclk

all:
	gcc -o $(LIB_NAME) -shared -fPIC -Isrc $(LOCAL_SRC) -DBOARD_${BOARD} -ggdb

install:
	cp $(LIB_NAME) $(PKG_DIR)/
	pip3 install .

test: all
	gcc -o $(TEST_EXE) -fPIC -Itest -Isrc $(TEST_SRC) -L. -l$(PKG_DIR)

clean:
	rm $(LIB_NAME)
