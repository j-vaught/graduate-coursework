#write a function that takes 4 arguments
#adds the first 2, subtracts the second 2, adds them together
#returns final value

.data
	#don't need any extra data
	newline: .asciiz "\n"
.text
	li $t0, 3

	li $a0, 10
	li $a1, 4
	li $a2, 3
	li $a3, 12
	jal math
	
	move $a0, $v0
	li $v0, 1
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall
	
	move $a0, $t0
	li $v0, 1
	syscall
	
exit:
	li $v0, 10
	syscall
	
math:
	#write the code
	#a0-a3
	#save the environment
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $t1, 4($sp)
	sw $t2, 8($sp)
	
	add $t0, $a0, $a1
	sub $t1, $a2, $a3
	add $t2, $t0, $t1
	move $v0, $t2
	
	#restore the environment
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	lw $t2, 8($sp)
	addi $sp, $sp, 12
	
	jr $ra
	
	
	