.data
	newline: .asciiz "\n"

.text
	#print number 6
	addi $v0, $zero, 1
	addi $a0, $zero, 6
	syscall
	
	#print newline
	addi $v0, $zero, 4
	la $a0, newline
	syscall
	
	#print number 3
	addi $v0, $zero, 1
	addi $a0, $zero, 3
	syscall