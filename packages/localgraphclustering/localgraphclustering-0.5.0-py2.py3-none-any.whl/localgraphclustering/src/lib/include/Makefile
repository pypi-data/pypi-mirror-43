UNAME := $(shell uname)
ifeq ($(UNAME),Linux)
	SHAREDLIB_EXT := so
	SHAREDLIB_FLAG := -shared
endif
ifeq ($(UNAME),Darwin)
	SHAREDLIB_EXT := dylib
	SHAREDLIB_FLAG := -dynamiclib
endif

MAXFLOW := max_flow

CC := $(CXX)
CXXFLAGS := -std=c++11 -Wall -O3 -Wshadow -fPIC

MAXFLOW_SRCS = maxflow.cpp test_max_flow.cpp
MAXFLOW_OBJS = $(MAXFLOW_SRCS:%.cpp=%.o)

all: $(MAXFLOW)


$(MAXFLOW): $(MAXFLOW_OBJS)
	$(CC) $(MAXFLOW_OBJS) -o $(MAXFLOW)


test:
	./find_densest_subgraph yeast-cc.smat
	./find_densest_subgraph pgp-cc.smat
	./find_densest_subgraph musm-cc.smat
	./find_densest_subgraph marvel-comics-cc.smat
	./find_densest_subgraph marvel-chars-cc.smat
	./find_densest_subgraph homo-cc.smat
	./find_densest_subgraph Erdos02-cc.smat
	./find_densest_subgraph as-caida20060911.smat
	./find_densest_subgraph as19991115.smat

.PHONY: all clean test

clean:
	$(RM) $(MAXFLOW) $(MAXFLOW_OBJS)
