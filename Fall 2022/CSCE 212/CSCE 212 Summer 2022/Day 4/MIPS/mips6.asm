#make a function that adds 2 numbers and returns them
#int test(a,b)
#    return a + b;
.data
	#where data is stored into memory
.text
	#reading int from user, moving to $t0
	li $v0, 5
	syscall
	move $t0, $v0
	
	#read second int from user, move to $t1
	li $v0, 5
	syscall
	move $t1, $v0
	
	#t0 and t1 have both user inputs
	move $a0, $t0
	move $a1, $t1
	jal addition
	#move returned value into t2
	move $t2, $v0
	
	#print t2
	li $v0, 1
	move $a0, $t2
	syscall
	
exit:
	#exit condition
	li $v0, 10
	syscall
	
addition:
	#write core code
	#check if anything could be used elsewhere
	#jr back to where we were
	#params: a0-a3
	#a0 = a, a1 = b
	#return values: v0, v1
	add $v0, $a0, $a1
	jr $ra
	
	
	
	