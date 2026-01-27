#A[]
#b
#for i -> b
#   print(A[i])
.data
	A: .space 20
	c: .word 32
	
.text
	la $t0, A	#t0 = &A
	
	li $t1, 5	#c = 5
	sw $t1, 0($t0)	#A[0] = c
	
	li $t1, 3
	sw $t1, 4($t0)
	
	li $t1, 1
	sw $t1, 8($t0)
	
	li $t1, 12
	sw $t1, 12($t0)
	
	li $t1, 15
	sw $t1, 16($t0)
	
	move $a0, $t0	#arg 1 = t0
	li $a1, 7	#arg 2 = 2
	jal example3
	
exit:
	li $v0, 10
	syscall
	
example3:
	#save environment
	addi $sp, $sp, -12
	sw $t0, 0($sp)
	sw $t1, 4($sp)
	sw $s0, 8($sp)
	#write code
	#A -> $a0
	#b -> $a1
	#move A into $s0 so we can print
	move $s0, $a0
	li $t0, 0	#i = 0
Loop:
	bge $t0, $a1, funcexit
	
	#get A[i]
	sll $t1, $t0, 2	#t1 = i * 4
	add $t1, $t1, $s0 #address of A[i]
	lw $a0, 0($t1)
	li $v0, 1
	syscall
	
	#newline
	
	addi $t0, $t0, 1
	j Loop
	
funcexit:
	lw $t0, 0($sp)
	lw $t1, 4($sp)
	lw $s0, 8($sp)
	addi $sp, $sp, 12
	jr $ra
	#restore environment 
	