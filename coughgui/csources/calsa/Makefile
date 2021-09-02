TARGET=calsa

INCDIR=-I./

CC=gcc
WARN=-Wall

PTHREAD=-pthread
ALSALIB=`pkg-config --cflags --libs alsa`
CCFLAGS=$(OPT) $(WARN) $(PTHREAD) $(ALSALIB) -pipe

LD=$(CC)
LDFLAGS=$(OPT) $(WARN) $(PTHREAD) $(ALSALIB) -export-dynamic

SOURCES=$(wildcard *.c )
OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

%.o: %.c
	$(CC) $(CCFLAGS) $(INCDIR) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJECTS)
