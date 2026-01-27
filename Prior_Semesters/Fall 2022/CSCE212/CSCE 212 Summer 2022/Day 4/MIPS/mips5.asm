.data
	newline: .asciiz "\n"

.text
	#for loop, print all numbers up to $s0
	addi $s0, $zero, 10
	addi $t0, $zero, 0
Loop:
	beq $s0, $t0, Exit
	#print $t0
	addi $v0, $zero, 1
	add $a0, $zero, $t0
	syscall
	
	addi $v0, $zero, 4
	la $a0, newline
	syscall
	
	#i++
	addi $t0, $t0, 1
	
	j Loop
	
Exit:
	addi $v0, $zero, 10
	syscall