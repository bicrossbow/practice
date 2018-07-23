//
//  main.c
//  variable_arguments
//
//  Created by Nu Zhang on 7/22/18.
//  Copyright © 2018 Nu Zhang. All rights reserved.
//

#include <stdio.h>
#include <stdarg.h>

/*
 #define _INTSIZEOF(n)   ((sizeof(n)+sizeof(int)-1)&~(sizeof(int) - 1) )
 #define va_start(ap,v) ( ap = (va_list)&v + _INTSIZEOF(v) )           //第一个可选参数地址
 #define va_arg(ap,t) ( *(t *)((ap += _INTSIZEOF(t)) - _INTSIZEOF(t)) ) //下一个参数地址
 #define va_end(ap)    ( ap = (va_list)0 )                            // 将指针置为无效
 */

const int INT_TYPE   = 100000;
const int STR_TYPE   = 100001;
const int CHAR_TYPE   = 100002;
const int LONG_TYPE   = 100003;
const int FLOAT_TYPE = 100004;
const int DOUBLE_TYPE = 100005;

int arg_varg_sum_int(int num_arg,...);
void arg_varg_diff_type(int num_arg,...);

int main(int argc, const char * argv[]) {
    int sum;
    printf("---Var Arg fixed INT type---\n");
    sum = arg_varg_sum_int(5,1,2,3,4,5);
    printf("sum = %d = arg_varg_sum_int(5,1,2,3,4,5)\n\n",sum);
    sum = arg_varg_sum_int(10,1,2,3,4,5,6,7,8,9,10);
    printf("sum = %d = arg_varg_sum_int(10,1,2,3,4,5,6,7,8,9,10)\n\n",sum);
    
    
    printf("*******************************\n\n");
    printf("---Var Arg different type---\n");
    arg_varg_diff_type(2,INT_TYPE,222,STR_TYPE,"a_string");
    
    return 0;
}

int arg_varg_sum_int(int num_arg,...)
{
    //va_start initializes an object of this type in such a way
    //that subsequent calls to va_arg sequentially retrieve
    //the additional arguments passed to the function.
    va_list arg_ptr;
    
    // #define va_start(ap,v) ( ap = (va_list)&v + _INTSIZEOF(v) )
    // the arg are saved in stack as:
    // last (N) rag
    // N-1 arg
    // ...
    // first arg
    // function returning address
    // function code section
    //
    va_start(arg_ptr,num_arg);// init varg_ptr to get the 1st varg start address
    int sum=0;
    int var;
    
    printf("&arg_varg_sum_int(%p)\n",arg_varg_sum_int);
    printf("&um_arg(%p)\n",&num_arg);
    
    printf("arg 0(%p):%d\n",arg_ptr,num_arg);
    for (size_t i=0; i<num_arg; ++i) {
        var = va_arg(arg_ptr, int);//get next var address
        printf("arg %lu(%p):%d\n",i+1,arg_ptr,var);
        sum += var;
    }
    va_end(arg_ptr);
    printf("va_end(%p)\n",arg_ptr);
    return sum;
}

void arg_varg_diff_type(int num_arg,...)
{
    int arg_type;
    int var_int;
    char* var_str;
    
    va_list arg_ptr;
    va_start(arg_ptr, num_arg);
    for (int i=0; i<num_arg; ++i) {
        arg_type = va_arg(arg_ptr, int);
        switch (arg_type) {
            case INT_TYPE:
                var_int = va_arg(arg_ptr, int);
                printf("arg %i(INT @%p): %d\n",i+1,arg_ptr,var_int);
                break;
            case STR_TYPE:
                var_str = va_arg(arg_ptr, char*);
                printf("arg %i(STR @%p): %s\n",i+1,arg_ptr,var_str);
            default:
                break;
        }
    }
    va_end(arg_ptr);
    printf("va_end(%p)\n",arg_ptr);
    return;
}
