CXXFLAGS += -Wall -O2 -funroll-loops `root-config --cflags --libs`
LDFLAGS += -lstdc++

SiphraReader: SiphraReader.cpp
	g++ SiphraReader.cpp -o build/SiphraReader $(CXXFLAGS) $(LDFLAGS)

clean:
	rm -f SiphraReader *~ *.o *.a
	rm -f build/*
