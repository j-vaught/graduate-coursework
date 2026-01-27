#
.data
	#no
	
.text
	#give function a value for argument
	li $a0, 3
	#return value will be $v0
	jal fact
	
	move $a0, $v0
	li $v0, 1
	syscall
	
exit:
	li $v0, 10
	syscall

fact:
	addi $sp, $sp, -8
	sw $a0, 0($sp)	#saving argument
	sw $ra, 4($sp)	#saving return spot
	
	slti $t0, $a0, 1
	beq $t0, $zero, L1
	
	li $v0, 1
	addi $sp, $sp, 8
	jr $ra
			
L1:
	addi $a0, $a0, -1
	jal fact
	lw $a0, 0($sp)
	lw $ra, 4($sp)
	addi $sp, $sp, 8
	mul $v0, $a0, $v0
	jr $ra