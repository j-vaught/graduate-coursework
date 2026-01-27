#example1(int a)
#    int b = a * a;
#    return b;
.data
	#nothing in .data
.text
	#setup for function
	li $a0, 9
	jal example1
	move $t0, $v0
	
	li $v0, 1
	move $a0, $t0
	syscall

exit:
	li $v0, 10
	syscall
		
example1:
	#store the environment
	addi $sp, $sp, -12
	sw $s0, 0($sp)
	sw $t0, 4($sp)
	sw $t1, 8($sp)
	#write function
	#a + a + a + a...a times
	move $s0, $a0	#put a into #s0
	li $t0, 1	#i = 0
	move $t1, $a0	#the value we are going up to, j
loop:
	bge $t0, $t1, funcexit
	add $s0, $s0, $a0	#sum = sum + a
	addi $t0, $t0, 1
	j loop
	
funcexit:
	#return value
	move $v0, $s0
	#code...
	lw $s0, 0($sp)
	lw $t0, 4($sp)
	lw $t1, 8($sp)
	addi $sp, $sp, 12
	
	jr $ra