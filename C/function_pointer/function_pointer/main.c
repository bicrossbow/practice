//
//  main.c
//  function_declaration
//
//  Created by Nu Zhang on 7/22/18.
//  Copyright © 2018 Nu Zhang. All rights reserved.
//

#include <stdio.h>

void fun1_int(void)
{
    printf("%s\n",__func__);
}

void fun2_int(void)
{
    printf("%s\n",__func__);
}

typedef void(*fun_ptr_def)(void);

int main(int argc, const char * argv[]) {
    // function pointer
    void (*func_ptr)(void);
    func_ptr = fun1_int;
    (*func_ptr)();
    
    func_ptr = fun2_int;
    (*func_ptr)();
    
    fun_ptr_def func_ptr_by_def;
    func_ptr_by_def = fun1_int;
    (*func_ptr_by_def)();
    
    func_ptr_by_def = fun2_int;
    (*func_ptr_by_def)();
    
    
    printf("end\n");
    return 0;
}
