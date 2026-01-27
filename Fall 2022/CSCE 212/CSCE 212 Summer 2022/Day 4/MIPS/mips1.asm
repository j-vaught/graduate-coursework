#a = 10, b = 5, c = a + b
#s0, s1, s2
.text
	addi $s0, $zero, 10
	#li $s0, 10
	addi $s1, $zero, 5
	#li $s1, 5
	add $s2, $s0, $s1
	
	#get 1 into $v0
	addi $v0, $zero, 1
	#li $v0, 1
	#get print number into $a0
	add $a0, $zero, $s2
	#move $a0, $s2
	syscall
	
	addi $v0, $zero, 1
	addi $a0, $zero, 12
	syscall