.data
	#no
.text
	li $a0, 39
	li $a1, 10
	jal example2
	
	move $a0, $v0
	li $v0, 1
	syscall
	
exit:
	li $v0, 10
	syscall
	
example2:
	#environment
	addi $sp, $sp, -8
	sw $s0, 0($sp)
	sw $s1, 4($sp)
	#code
	#c = a * 2
	sll $s0, $a0, 1
	#d = b * 2
	sll $s1, $a1, 1
	add $v0, $s0, $s1
	
	lw $s0, 0($sp)
	lw $s1, 4($sp)
	addi $sp, $sp, 8
	
	jr $ra
	
	
