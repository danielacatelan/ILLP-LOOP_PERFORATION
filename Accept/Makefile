ACCEPT_DIR ?= ../../accept
include $(ACCEPT_DIR)/accept.mk
LIBS := -lm -liomp5

SOURCES := pi.c
SOMADOR := addx

BIBLIOTECAS = $(ACCEPT_DIR)/include
NAME := $(basename $(SOURCES))
MOD_NAME := $(addsuffix _modificado.c, $(NAME))
OUTPUT := $(addsuffix _$(SOMADOR), $(NAME))
ARQUIVOS_PARA_REMOVER := $(MOD_NAME) *$(SOMADOR) *.bc *.s

construir_addx:
	$(MAKE) limpar
	$(MAKE) build_orig OPTARGS="-all-lpe"
	nano accept_config.txt
	$(MAKE) pause
	python $(ACCEPT_DIR)/script.py $(SOMADOR)

	ls > temp.txt
	if grep -q $(MOD_NAME) temp.txt; then \
    		riscv32-unknown-elf-gcc $(MOD_NAME) -O1 -march=rv32im -o $(OUTPUT) -lm -I $(BIBLIOTECAS) \
        		$(eval export PATH=$(PATH):/opt/riscv/bin); \
        else \
    			riscv32-unknown-elf-gcc $(SOURCES) -O1 -march=rv32im -o $(OUTPUT) -lm -I $(BIBLIOTECAS) \
        	$(eval export PATH=$(PATH):/opt/riscv/bin); \
        fi
	rm temp.txt

	clear
	spike --isa=RV32I /opt/riscv/riscv32-unknown-elf/bin/pk $(OUTPUT)


construir_accept:
	$(MAKE) limpar
	$(MAKE) build_orig OPTARGS="-all-lpe"
	nano accept_config.txt
	$(MAKE) pause
	$(MAKE) build_opt
	

construir_accept_spike:
	$(MAKE) limpar
	$(MAKE) construir_accept
	/usr/lib/llvm-10/bin/llc  -O2  -march=riscv32 -filetype=asm app.opt.bc -o $(NAME).s
	riscv32-unknown-elf-gcc $(NAME).s -O1 -march=rv32im -o $(OUTPUT) -lm \
			$(eval export PATH=$(PATH):/opt/riscv/bin)
	time spike --isa=RV32I /opt/riscv/riscv32-unknown-elf/bin/pk $(OUTPUT) \
			$(eval export PATH=$(PATH):/opt/riscv/bin)
	

pause:
	@echo "Modificou accept_config.txt?"
	@read dummy
	
limpar:
	$(MAKE) clean
	$(foreach arq,$(ARQUIVOS_PARA_REMOVER), \
		if [ -n "$(wildcard $(arq))" ]; then rm $(arq); fi; \
	)
