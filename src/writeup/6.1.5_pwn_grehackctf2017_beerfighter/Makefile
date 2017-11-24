SRC_DIR = src
INC_DIR = inc
OBJ_DIR = obj
BIN_DIR = bin
OUT_DIR = $(OBJ_DIR) $(BIN_DIR)

CC = gcc
LD = gcc
INC = -I $(INC_DIR)
DEBUGFLAG=-g
CFLAGS= $(INC) -nostdlib -fno-stack-protector -Wl,-z,relro,-z,now,-z,noexecstack -static -Wno-builtin-declaration-mismatch -s
LDFLAGS= -nostdlib -fno-stack-protector -Wl,-z,relro,-z,now,-z,noexecstack -static -Wno-builtin-declaration-mismatch -s

MKDIR_P = mkdir -p


.PHONY: directories


OBJ_FILES = $(OBJ_DIR)/main.o $(OBJ_DIR)/io.o $(OBJ_DIR)/strings.o $(OBJ_DIR)/lib.o
ASM_FILES = $(SRC_DIR)/syscalls.S $(SRC_DIR)/start.S $(SRC_DIR)/gadgets.S

TARGET = $(BIN_DIR)/aaaaaa

all: directories $(TARGET)

directories: $(OUT_DIR)

$(OUT_DIR):
	$(MKDIR_P) $(OUT_DIR)

$(TARGET): $(OBJ_FILES)
	$(LD) $(LDFLAGS) $(OBJ_FILES) $(ASM_FILES) -o $(TARGET)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.c $(INC_DIR)/*.h
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJ_FILES) $(BIN_DIR)/*
