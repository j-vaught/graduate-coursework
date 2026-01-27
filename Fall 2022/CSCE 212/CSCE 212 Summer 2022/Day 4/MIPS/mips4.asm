.data
	prompt: .asciiz "Type in a number: "
	message: .asciiz "Your number will be multiplied by 2."
	message2: .asciiz "Your new value is: "
	newline: .asciiz "\n"

.text
	addi $v0, $zero, 4
	la $a0, prompt
	syscall

	#read int
	addi $v0, $zero, 5
	syscall
	
	#move user input into real register
	#s0 is user input 1
	add $s0, $zero, $v0
	
	addi $v0, $zero, 4
	la $a0, message
	syscall
	
	addi $v0, $zero, 4
	la $a0, newline
	syscall
	
	addi $v0, $zero, 4
	la $a0, message2
	syscall
	
	sll $a0, $s0, 1
	addi $v0, $zero, 1
	syscall
	
exit:
	addi $v0, $zero, 10
	syscall