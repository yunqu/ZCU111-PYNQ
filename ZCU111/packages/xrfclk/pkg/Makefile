LOCAL_SRC := $(wildcard src/*.c)
TEST_SRC := $(wildcard test/*.c)
PKG := xrfclk
LIB_NAME := lib$(PKG).so
TEST_EXE := test.elf

all:
	gcc -o $(LIB_NAME) -shared -fPIC -Isrc $(LOCAL_SRC) -DBOARD_${BOARD} -ggdb

install:
	cp $(LIB_NAME) $(PKG)/
	pip3 install .

test: all
	gcc -o $(TEST_EXE) \
		-fPIC -Itest -Isrc $(TEST_SRC) -L. -l$(PKG) -DBOARD_${BOARD}
	cp -rf $(LIB_NAME) /usr/lib

clean:
	rm -rf $(LIB_NAME) $(TEST_EXE)
	rm -rf /usr/lib/$(LIB_NAME)
