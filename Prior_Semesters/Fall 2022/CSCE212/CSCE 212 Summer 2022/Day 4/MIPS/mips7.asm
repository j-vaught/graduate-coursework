#Function that prints a newline

.data
	newline: .asciiz "\n"
.text
	#we need to print int
	#make new line
	#print another int
	li $v0, 1
	li $a0, 10
	syscall
	
	jal nl
	
	li $v0, 1
	li $a0, 8
	syscall
	
exit:
	li $v0, 10
	syscall
	
nl:
	#write code first...
	li $v0, 4
	la $a0, newline
	syscall
	jr $ra
	
print_string:
	li $v0, 4
	#a0 loaded before jal
	syscall
	jr $ra