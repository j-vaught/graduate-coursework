#include <stdio.h>
//Jacob Vaught
//CSCE 212
int main(){
    int num1,num2;
    printf("Enter the Number 1: ");
    scanf("%d", &num1);
    printf("Enter the Number 2: ");
    scanf("%d", &num2);
    printf("\n");
    printf("Number 1 = %d; Number 2 = %d", num1, num2);
    printf("\n");
    printf("%d & %d = %d", num1, num2, num1 & num2);
    printf("\n");
    printf("%d | %d = %d", num1, num2, num1 | num2);
    printf("\n");
    printf("%d ^ %d = %d", num1, num2, num1 ^ num2);
    printf("\n");
    printf("%d << 1 = %d", num1, num1 << 1);
    printf("\n");
    printf("%d >> 1 = %d", num1, num1 >> 1);
    printf("\n");
    printf("~ %d = %d", num1, ~num1);
    printf("\n");
    printf("%d << 1 = %d", num2, num2 << 1);
    printf("\n");
    printf("%d >> 1 = %d", num2, num2 >> 1);
    printf("\n");
    printf("~ %d = %d", num2, ~num2);
    return 0;
}