TARGET=cough

INCDIR=-I./

CC=gcc
WARN=-Wall

PTHREAD=-pthread
GTKLIB=`pkg-config --cflags --libs gtk+-3.0`
CCFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) -pipe

LD=$(CC)
LDFLAGS=$(OPT) $(WARN) $(PTHREAD) $(GTKLIB) -export-dynamic

SOURCES=$(wildcard *.c )
OBJECTS=$(SOURCES:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(LD) $(OBJECTS) $(LDFLAGS) -o $(TARGET)

%.o: %.c
	$(CC) $(CCFLAGS) $(INCDIR) -c -o $@ $<

clean:
	rm -f $(TARGET) $(OBJECTS)
