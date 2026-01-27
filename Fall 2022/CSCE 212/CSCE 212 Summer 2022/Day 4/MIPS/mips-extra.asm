.data
	#array
	#for every element, we add 4
	array: .space 20
	
	newline: .asciiz "\n"
.text
	li $t0, 0	#j
	li $s0, 5	#goal for j
	
	li $t1, 0	#i
	li $s1, 3	#goal for i

	
#condition to jump over loop
#for(int i = 0; i < 3; i++)
#	for(int j = 0; j < 5; j++)
#		print(j)
loop:
	li $t0, 0	#resets the internal for loop
	#could check condition here
	loop2:
		li $v0, 1
		move $a0, $t0
		syscall
	
		la $a0, newline
		li $v0, 4
		syscall
	
		addi $t0, $t0, 1
		blt $t0, $s0, loop2
	addi $t1, $t1, 1
	blt $t1, $s1, loop
	
	

exit:
	li $v0, 10
	syscall
	
	
	
	