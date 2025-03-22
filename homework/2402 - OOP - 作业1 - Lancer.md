### 2402 - OOP - 作业1 - Lancer

------

#### 判断题

1.面向对象程序设计的继承性鼓励程序员重用被实践验证的高质量软件。(T)

2.Python语言可以用面向对象的方法编程。  (T)

3.面向对象的程序设计方法模仿计算机的工作方式，程序被视为一序列依次执行的指令。(F) 原因：面向过程

4.面向对象是基于面向过程的。(F) 原因：二者相互独立，不存在谁基于谁

------

#### 单选题

1.(  )运算符不能用于非整型数据运算

A. /    **B. %**    C. *    D. ++

2.下列运算符中，(  )既可以做单目运算符，又可以做双目运算符

A. new    **B. +**    C. <=    D. &&

3.符号>、<、==都是(  )运算符

**A. 关系**    B. 逻辑    C. 条件    D. 三元

4.设E为表达式，以下与do{}while(E);不等价的语句是(  )

A. do{}while(!E == 0)    B. do{}while(E > 0 || E < 0)    **C. do{}while(E == 0)**    D. do{}while(E != 0)

5.结构化程序所要求的基本控制结构不包括(  )

A. 顺序结构    **B. 嵌套**    C. 选择结构    D. 循环结构

------

#### 填空题

1.以下程序的运行结果是( <u>123213321</u> )

```c
#include <stdio.h>
struct st{
  char c; 
  char s[80];
};
struct  st a[4] = {{'1',"123"}, {'2',"321"}, {'3',"123"}, {'4',"321"}};
char * f(struct st *t);

int main( )
{  int k;

  for(k = 0; k < 4; k++){
    printf("%s", f(a+k));
  }

  return 0;
}

char * f(struct st *t)
{   
   int k = 0;
    
   while(t->s[k] != '\0'){
        if( t->s[k] == t->c){
          return t->s+k;
        }
        k++;
    }
        
   return t->s;
}
```

2.以下为一段伪代码*~~(已将其翻译成C语言)~~*，请写出其运行结果( <u>5</u> )

```c
a = 1;
for(int b = 1; b <= 9; b++){
    if(a >= 8)break;
    if(a % 2 == 1){
        a += 2;
        continue;
    }
    a = 3;
}
printf("%d", b);
```

------

#### 程序填空题

*空的部分在程序中用额外的小括号括起*

1.输入一个十进制整数a，然后输入一个n(n为2、8或16)，将a转换为n进制数据输出。

```c
#include <stdio.h>
int main(){
    unsigned int a, n, i = 0;
    int arr[100] = { 0 };
    scanf ("%d %d", &a, &n);
    if (n != 2 && n != 8 && n != 16)
        return 0;
    do {
        arr[i++] = (a % n);//第一个空
        (a /= n);//第二个空
    }while (a != 0);
    
    while (i > 0)
    {
        if ( (arr[--i] == 16) )//第三个空，重点
            printf ("%c", 'A' + arr[i] - 10);
        else
            printf ("%d", arr[i]);
    }
    
    return 0;
}
```

2.本程序的功能是：从键盘输入一行字符，以回车结束，统计其中英文字母、数字字符、其他字符的个数（不含末尾的回车符）。

输入样例：afc34*@8 th(

输出样例：letters=5,digits=3,others=4

```c
#include <stdio.h>
 
int main()    
{ 
    int letters=0, digits=0, others=0;
    char ch;
    while(  (ch=getchar()) != ('\n') )//第一个空
    {
        if( ch>='A'&&ch<='Z' || (ch >= 'a' && ch <= 'z') )//第二个空
            letters++;
        else if ( (ch >= '0' && ch <= '9') )//第三个空
            digits++;
        else
        	(others++);//第四个空
    }
    printf("letters=%d,digits=%d,others=%d\n", (letters, digits, others) );//第五个空
    return 0;
}
```

3.请填空，让以下程序输出100以内的所有素数，每个素数一行。

注意：填空的内容可能有些反直觉。~~*怀疑是出错了，无所谓，我会引号匹配*~~

```c
#include <stdio.h>
#include <math.h>
int main(){
    for(int i=2;i<100;i++){
        int is_prime = 1;
        for(int j=2; j*j (<=) i; j++){//第一个空
            if(i%j==0){ is_prime=0; break;}
        }
        if(is_prime){
            printf("(%d\n",i,")");//第二个空，在直觉上没有传参的地方输出变量吗，哈吉侯，你这家伙... 很简单，我传空串不就是了
        }
    }
    return 0;
}
```

4.请填写空缺的代码，完成后的代码应具有以下功能：
1）依次将10个整数输入给数组a;
2）从数组a的10个元素中找到最小值并输出。

```c
#include <stdio.h>
int main()
{
    int a[10];
    for(int i=0; i<10; i++)
    {
        (scanf("%d", &a[i]);)//第一个空
    }
    int min;
    (min = a[0];)//第二个空
    for(int i=1; i<10; i++)
    {
        if( (a[i] < min) )//第三个空
        {
            (min = a[i];)//第四个空
        }
    }
    printf("%d\n", min);
    return 0;
}
```

------

#### 函数题

##### 1.本题要求实现一个根据学生成绩设置其等级，并统计不及格人数的简单函数。

**函数接口定义:**

```c
int set_grade( struct student *p, int n );
```

其中`p`是指向学生信息的结构体数组的指针，该结构体的定义为:

```c
struct student{
    int num;
    char name[20];
    int score;
    char grade;
};
```

`n`是数组元素个数。学号`num`、姓名`name`和成绩`score`均是已经存储好的。`set_grade`函数需要根据学生的成绩`score`设置其等级`grade`。等级设置：85－100为A，70－84为B，60－69为C，0－59为D。同时，`set_grade`还需要返回不及格的人数。

**裁判测试程序样例：**

```c
#include <stdio.h>
#define MAXN 10

struct student{
    int num;
    char name[20];
    int score;
    char grade;
};

int set_grade( struct student *p, int n );

int main()
{   struct student stu[MAXN], *ptr;
    int n, i, count;
    
    ptr = stu;
    scanf("%d\n", &n);
    for(i = 0; i < n; i++){
       scanf("%d%s%d", &stu[i].num, stu[i].name, &stu[i].score);
    } 
   count = set_grade(ptr, n);
   printf("The count for failed (<60): %d\n", count);
   printf("The grades:\n"); 
   for(i = 0; i < n; i++)
       printf("%d %s %c\n", stu[i].num, stu[i].name, stu[i].grade);
    return 0;
}

/* 你的代码将被嵌在这里 */
```

**输入样例：**

```in
10
31001 annie 85
31002 bonny 75
31003 carol 70
31004 dan 84
31005 susan 90
31006 paul 69
31007 pam 60
31008 apple 50
31009 nancy 100
31010 bob 78
```

**输出样例:**

```out
The count for failed (<60): 1
The grades:
31001 annie A
31002 bonny B
31003 carol B
31004 dan B
31005 susan A
31006 paul C
31007 pam C
31008 apple D
31009 nancy A
31010 bob B
```

**code:**

```c
int set_grade(struct student *p, int n){
    int cnt = 0;
    for(int i = 0; i < n; i++){
        if((p+i)->score >= 85){
            (p+i)->grade = 'A';
        }else if((p+i)->score >= 70){
            (p+i)->grade = 'B';
        }else if((p+i)->score >= 60){
            (p+i)->grade = 'C';
        }else{
            (p+i)->grade = 'D';
            cnt++;
        }
    }
    return cnt;
}
```

##### 2.求任意n个整数中的奇数的和。

**函数接口定义:**

```c
int fun(int a[ ],int n);
```

其中`a[]` 是用户传入的一个数组； `n` 是用户传入的一个整数；函数fun的功能是计算并返回数组 `a` 的前 `n` 个数中的奇数的和。

**裁判测试程序样例:**

```c
#include<stdio.h> 
#define N 100
int fun(int a[ ], int n);

int main( )
 {  int b[N],  m,  i,  s;
    scanf("%d", &m);
    for(i=0;  i<m;  i++)   
        scanf("%d", &b[i]);
    s=fun(b, m);
    printf("s=%d\n",s);
    return 0;
 }

/* 你编写的函数将嵌入在这里 */
```

**输入样例:**

```in
10
11 12 13 14 15 16 17 18 19 20
```

**输出样例:**

```out
s=75
```

**code:**

```c
int fun(int a[ ],int n){
    int ans = 0;
    for(int i = 0; i < n; i++){
        if(a[i] % 2 == 1){
            ans += a[i];
        }
    }
    return ans;
}
```

------

#### 编程题

##### 1.宇宙无敌加法器

地球人习惯使用十进制数，并且默认一个数字的每一位都是十进制的。而在 PAT 星人开挂的世界里，每个数字的每一位都是不同进制的，这种神奇的数字称为“PAT数”。每个 PAT 星人都必须熟记各位数字的进制表，例如“……0527”就表示最低位是 7 进制数、第 2 位是 2 进制数、第 3 位是 5 进制数、第 4 位是 10 进制数，等等。每一位的进制 d 或者是 0（表示十进制）、或者是 [2，9] 区间内的整数。理论上这个进制表应该包含无穷多位数字，但从实际应用出发，PAT 星人通常只需要记住前 20 位就够用了，以后各位默认为 10 进制。

在这样的数字系统中，即使是简单的加法运算也变得不简单。例如对应进制表“0527”，该如何计算“6203 + 415”呢？我们得首先计算最低位：3 + 5 = 8；因为最低位是 7 进制的，所以我们得到 1 和 1 个进位。第 2 位是：0 + 1 + 1（进位）= 2；因为此位是 2 进制的，所以我们得到 0 和 1 个进位。第 3 位是：2 + 4 + 1（进位）= 7；因为此位是 5 进制的，所以我们得到 2 和 1 个进位。第 4 位是：6 + 1（进位）= 7；因为此位是 10 进制的，所以我们就得到 7。最后我们得到：6203 + 415 = 7201。

**输入格式:**

输入首先在第一行给出一个 N 位的进制表（0 < N ≤ 20），以回车结束。 随后两行，每行给出一个不超过 N 位的非负的 PAT 数。

**输出格式:**

在一行中输出两个 PAT 数之和。

**输入样例:**

```in
30527
06203
415
```

**输出样例:**

```out
7201
```

**code:**

```c++
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
class Solution{
public:
    string addPATNumbers(const string& base, const string& num1, const string& num2){
        string reversedBase = base;
        reverse(reversedBase.begin(), reversedBase.end());
        string reversedNum1 = num1;
        reverse(reversedNum1.begin(), reversedNum1.end());
        string reversedNum2 = num2;
        reverse(reversedNum2.begin(), reversedNum2.end());
        int maxLength = max({reversedBase.size(), reversedNum1.size(), reversedNum2.size()});
        reversedBase.resize(maxLength, '0');
        reversedNum1.resize(maxLength, '0');
        reversedNum2.resize(maxLength, '0');
        string result;
        int carry = 0;
        for(int i = 0; i < maxLength; i++){
            int digit1 = reversedNum1[i] - '0';
            int digit2 = reversedNum2[i] - '0';
            int baseDigit = reversedBase[i] - '0';
            if (baseDigit == 0) baseDigit = 10;
            int sum = digit1 + digit2 + carry;
            if(sum >= baseDigit){
                carry = 1;
                sum -= baseDigit;
            }else{
                carry = 0;
            }
            result += to_string(sum);
        }
        if(carry > 0){
            result += to_string(carry);
        }
        reverse(result.begin(), result.end());
        result.erase(0, min(result.find_first_not_of('0'), result.size() - 1));
        return result;
    }
};
int main(){
    string base, num1, num2;
    getline(cin, base);
    getline(cin, num1);
    getline(cin, num2);
    Solution solution;
    cout << solution.addPATNumbers(base, num1, num2);
    return 0;
}
```

##### 2.高斯的日记

数学家高斯写日记，从不写年月日，而是写一个整数。后来人们才知道，这个整数就是日期，是高斯出生后的第几天。这也许是个好习惯，它时刻提醒着主人：日子又过去一天，光阴似箭呐！

高斯是 1777 年 4 月 30 日出生的。高斯发现一个重要定理那天日记上写着 5343，那天是 1791 年 12 月 15 日。高斯获得博士学位那天日记上写着 8113，那天是哪一天呢？

请编写程序，输入高斯日记上的整数，输出对应的日期。

**输入格式:**

整数

**输出格式:**

日期

**输入样例:**

```im
5343
```

**输出样例:**

```out
1791/12/15
```

**code:**

```c++
#include <iostream>
#include <cmath>
#include <string>
using namespace std;
class Solution{
private:
    int isLeapYear(int year){
        return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    }
    int daysInMonth(int year, int month){
        int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
        if(month == 2 && isLeapYear(year)){
            return 29;
        }
        return days[month - 1];
    }
public:
    string calculateDate(int days){
        int year = 1777;
        int month = 4;
        int day = 30;
        for(int i = 1; i < days; i++){
            day++;
            if(day > daysInMonth(year, month)){
                day = 1;
                month++;
                if(month > 12){
                    month = 1;
                    year++;
                }
            }
        }
        char buffer[20];
        sprintf(buffer, "%04d/%02d/%02d", year, month, day);
        return string(buffer);
    }
};
int main(){
    int days;
    cin >> days;
    Solution s;
    cout << s.calculateDate(days);
    return 0;
}
```

------

#### 主观题

100层楼，2个鸡蛋，设计算法确定最少需要试几次能确保知道哪层落下不会碎？

**个人答案:**

```ans
假设最优的尝试次数为x次，则第一次扔在第x+1层，如果碎了，那么第二个从第1层重新遍历，共尝试x+1次，和假设尝试x次相悖，因此第一次扔的楼层必须小于x+1层。

假设第一次扔在第x-1层，如果碎了，那么第二个从第1层重新遍历，一直扔到第x-2层，共尝试x-2+1 = x-1次。

假设第一次扔在第x层，如果碎了，那么第二个鸡蛋从第1层重新遍历，一直扔到第x-1层，共尝试了x-1+1 = x次，刚好没有超出假设次数。

因此，要想尽可能使楼层跨度大一些，又要保证不超过假设的尝试次数x，那么第一次扔鸡蛋的最优选择就是第x层。

可列出x + (x-1) + (x-2) + ... + 1 = 100，化简为(x+1)*x/2 = 100

最终ceil(x)= 14即最优解在最坏情况的尝试次数是14次，第一次扔鸡蛋的楼层也是14层。

```
