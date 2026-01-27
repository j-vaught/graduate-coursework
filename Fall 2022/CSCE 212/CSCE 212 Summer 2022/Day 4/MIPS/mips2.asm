.data
	test: .asciiz "Hello, World!"

.text
	addi $v0, $zero, 4
	#li $v0, 4
	la $a0, test
	
	syscall
