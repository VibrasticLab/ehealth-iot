# beside need Gtk3 and Cairo, it also need Slope Library
# For ArchLinux/Manjaro: https://github.com/mekatronik-achmadi/archmate/tree/master/packages/pkgbuild/gtk-slope/
# 
# For 'dmic_sv' setup to I2SMic volume: https://github.com/mekatronik-achmadi/archmate/blob/master/embedded/raspberrypi/install_armv7h.md#boost-i2s-mic-alsa
# To run: startx ./cough dmic_sv

TARGET=cough

INCDIR=-I./

CC=gcc
WARN=-Wall

PTHREAD=-pthread
ALSALIB=`pkg-config --cflags --libs alsa`
GTKLIB=`pkg-config --cflags --libs gtk+-3.0`
CCFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) $(ALSALIB) -pipe

LD=$(CC)
LIBFLAGS=-lm -lslope
LDFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) $(ALSALIB) $(LIBFLAGS) -export-dynamic

SOURCES=$(wildcard *.c )
OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

%.o: %.c
	$(CC) $(CCFLAGS) $(INCDIR) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJECTS)
