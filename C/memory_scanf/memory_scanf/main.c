//
//  main.c
//  memory_scanf
//
//  Created by Nu Zhang on 9/13/18.
//  Copyright © 2018 Nu Zhang. All rights reserved.
//

#include <stdio.h>

int main(int argc, const char * argv[]) {
    int i;
    char c;
    for(i=0;i<5;i++){
        scanf("%d",&c);
        printf("%d ",i);
    }
    return 0;
}
