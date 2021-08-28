# beside need Gtk3 and Cairo, it also need Slope Library
# For ArchLinux/Manjaro: https://github.com/mekatronik-achmadi/archmate/tree/master/packages/pkgbuild/gtk-slope/

TARGET=cough

INCDIR=-I./

CC=gcc
WARN=-Wall

PTHREAD=-pthread
GTKLIB=`pkg-config --cflags --libs gtk+-3.0`
CCFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) -pipe

LD=$(CC)
LIBFLAGS=-lm -lslope
LDFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) $(LIBFLAGS) -export-dynamic

SOURCES=$(wildcard *.c )
OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

%.o: %.c
	$(CC) $(CCFLAGS) $(INCDIR) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJECTS)
