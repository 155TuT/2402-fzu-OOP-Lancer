### 2402 - OOP - 作业2 - Lancer

------

#### 判断题

1.int (*p)[4]它表示p是一个指针数组，它包含4个指针变量元素。  (F) 原因: 应为int *p[4]，题中写法为正常数组

2.指针数组的每个元素都是一个指针变量。  (T)

3.char *s="C Language";表示s是一个指向字符串的指针变量，把字符串的首地址赋予s。  (T) 

4.不同类型的指针变量是可以直接相互赋值的。  (F) 原因: 类型安全，需要显式类型转换

5.假设结构指针p已定义并正确赋值，其指向的结构变量有一个成员是int型的score，则语句 p->score=99; 是正确的。  (T)

6.用链表代替数组进行数据操作时，查询更加方便。  (F) 原因: 链表需要从头节点的地址开始遍历，而数组可直接访问下标

7.通过命名空间可以区分具有相同名字的函数。  (T)

8.符号常量在定义时一定要初始化。  (T)

9.C++程序中，类的构造函数名与类名相同。  (T)

------

#### 单选题

1.在下列关键字中,用以说明类中公有成员的是(  )

**A. public**    B. private    C. protected    D. friend

2.有关类和对象的说法下列不正确的有(  )

A. 对象是类的一个实例    B. 任何对象只能属于一个具体的类    **C. 一个类只能有一个对象**    D. 类与对象和关系与数据类型和变量的关系相似

3.如果类定义中没有使用 private、protected、或public 关键字，则所有成员(  )

A. 都为public    B. 都为protected    **C. 都为private**    D. 不一定

4.有如下语句序列：

```c
char str[10];  cin>>str;
```

当从键盘输入"This is a  program"时，str数组得到的字符串是(  )

A. "This is a  progamm"    B. "This is a"    **C. "This"**    D. "This is"

5.在C++中，有语句`string t;`，则可输入一个包含空格的字符串到变量t中的语句是(  )

A. `cin >> t;`    **B. `getline(cin, t);`**    C. `gets(t);`    D. `scanf("%s", t);`

6.结构体类型S拥有字符数组成员name，若有定义语句“S s[10];”，则输出该数组的第3个元素的name的语句，错误的是(  )

A. `puts(s[3].name);`    B.`printf("%s",s[3].name);`    C. `cout<<s[3].name;`    **D. `cout<<s[3];`**

7.链表不具有的特点是(  )

A. 插入、删除不需要移动元素    **B.可随机访问任一元素**    C. 不必事先估计存储空间    D. 所需空间与线性长度成正比

8.在一个单链表head中，若要在指针p所指结点后插入一个q指针所指结点，则执行(  )

A. `p->next=q->next; q->next=p;`    B.`q->next=p->next; p=q;`    C. `p->next=q->next; p->next=q;`    **D. `q->next=p->next; p->next=q;`**

9.以下程序的输出结果是(  )

```c
#include <stdio.h>

struct HAR{
    int x, y; 
    struct  HAR  *p;
} h[2];

int main(void)
{ 
    h[0].x = 1; h[0].y = 2;
    h[1].x = 3; h[1].y = 4;
    h[0].p = h[1].p = h;
    printf("%d%d\n", (h[0].p)->x, (h[1].p)->y);

    return 0;        
}
```

**A. 12**    B. 23    C. 14    D. 32

------

#### 程序填空题

*空的部分在程序中用额外的小括号括起*

1.已建立英语课程的成绩链表，头指针为 *h**e**a**d*，其中成绩存于 *score* 域，学号存于 *n**u**m* 域，函数`Require(head)`的功能是在头指针为 *h**e**a**d* 的成绩链表中，找到并输出所有不及格学生的学号和成绩，以及统计并输出补考学生人数。

```c
void Require(struct student *head)
{
    int cnt;
    struct student *p;

     if ( head != NULL ) {
         cnt = 0;
         (p = head);//第一个空
         while (p != NULL) {
             if((p->score < 60)){//第二个空
                 printf ("%d %.1f\n", p->num, p->score); 
                 cnt++; 
             }
             (p++);//第三个空
         }
         printf ("%d\n", cnt);
      }
  }
```

2.结构体定义如下：

```c
struct ListNode{
   int data;
   struct ListNode *next;
};
```

本题目要求补全函数`deletem`将单链表`L`中所有存储了`m`的结点删除。返回指向结果链表头结点的指针。

```c
struct ListNode *deletem( struct ListNode *L, int m ) 
{
    struct ListNode *head,*p1,*p2;
    head=L;
    while((head != NULL) && head->data==m)//第一个空
    {
        (p2 = head);//第二个空
        head=head->next;
        free(p2);
    }
    if(head==NULL) return head; 
    p1=head;  
    p2=head->next;
    while((p2 != NULL))//第三个空
    {
        if(p2->data == m)  
        {
            p1->next=p2->next;
            (free(p2));//第四个空
            p2=p1->next; 
        }
        else  
        {
            p1=p2;
            p2=p2->next;
        }
    }
    return head;
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

##### 2.本题要求实现一个简单函数，找出两个数中的最大值。

**函数接口定义:**

```c
void findmax(int *px, int *py, int *pmax);
```

其中`px`和`py`是用户传入的两个整数的指针。函数`findmax`应找出两个指针所指向的整数中的最大值，存放在`pmax`指向的位置。

**裁判测试程序样例:**

```c
#include <stdio.h>

void findmax( int *px, int *py, int *pmax );

int main()
{    
    int max, x, y; 

    scanf("%d %d", &x, &y);
    findmax( &x, &y, &max );
    printf("%d\n", max);

    return 0;
} 

/* 你的代码将被嵌在这里 */
```

**输入样例:**

```in
3 5
```

**输出样例:**

```out
5
```

**code:**

```c
void findmax(int *px, int *py, int *pmax){
    *pmax = *px > *py ? *px : *py;
    return;
}
```

##### 3.本题要求实现两个函数，分别将读入的数据存储为单链表、将链表中偶数值的结点删除。

**函数接口定义:**

```c
struct ListNode *createlist();
struct ListNode *deleteeven(struct ListNode *head);
```

链表节点定义如下:

```c
struct ListNode {
    int data;
    struct ListNode *next;
};
```

函数`createlist`从标准输入读入一系列正整数，按照读入顺序建立单链表。当读到−1时表示输入结束，函数应返回指向单链表头结点的指针。

函数`deleteeven`将单链表`head`中偶数值的结点删除，返回结果链表的头指针。

**裁判测试程序样例：**

```c
#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int data;
    struct ListNode *next;
};

struct ListNode *createlist();
struct ListNode *deleteeven( struct ListNode *head );
void printlist( struct ListNode *head )
{
     struct ListNode *p = head;
     while (p) {
           printf("%d ", p->data);
           p = p->next;
     }
     printf("\n");
}

int main()
{
    struct ListNode *head;

    head = createlist();
    head = deleteeven(head);
    printlist(head);

    return 0;
}

/* 你的代码将被嵌在这里 */
```

**输入样例：**

```in
1 2 2 3 4 5 6 7 -1
```

**输出样例:**

```out
1 3 5 7 
```

**code:**

```c
struct ListNode *createlist(){
    struct ListNode *head = NULL;
    struct ListNode *tail = NULL;
    int tmpnum;
    scanf("%d", &tmpnum);
    while(tmpnum != -1){
        struct ListNode *node = (struct ListNode*)malloc(sizeof(struct ListNode));
        node->data = tmpnum;
        node->next = NULL;
        if(head == NULL){
            head = tail = node;
        }else{
            tail->next = node;
            tail = node;
        }
        scanf("%d", &tmpnum);
    }
    return head;
}
struct ListNode *deleteeven(struct ListNode *head){
    while(head != NULL && (head->data) % 2 == 0){
        struct ListNode *temp = head;
        head = head->next;
        free(temp);
    }
    if(head == NULL){
        return NULL;
    }
    struct ListNode *prev = head;
    struct ListNode *curr = head->next;
    while(curr != NULL){
        if((curr->data)% 2 == 0){
            prev->next = curr->next;
            free(curr);
            curr = prev->next;
        }else{
            prev = curr;
            curr = curr->next;
        }
    }
    return head;
}
```

------

#### 编程题

##### 1.找出总分最高的学生

给定N个学生的基本信息，包括学号（由5个数字组成的字符串）、姓名（长度小于10的不包含空白字符的非空字符串）和3门课程的成绩（[0,100]区间内的整数），要求输出总分最高学生的姓名、学号和总分。

**输入格式:**

输入在一行中给出正整数N（≤10）。随后N行，每行给出一位学生的信息，格式为“学号 姓名 成绩1 成绩2 成绩3”，中间以空格分隔。

**输出格式:**

在一行中输出总分最高学生的姓名、学号和总分，间隔一个空格。题目保证这样的学生是唯一的。

**输入样例:**

```in
5
00001 huanglan 78 83 75
00002 wanghai 76 80 77
00003 shenqiang 87 83 76
10001 zhangfeng 92 88 78
21987 zhangmeng 80 82 75
```

**输出样例:**

```out
zhangfeng 10001 258
```

**code:**

```c++
#include <iostream>
#include <string>
using namespace std;
string num, name;
int s, s1, s2, s3, n;
int main(){
    cin >> n;
    n--;
    cin >> num >> name >> s1 >> s2 >> s3;
    s = s1 + s2 + s3;
    while(n--){
        string tmpnum, tmpname;
        int tmps1, tmps2, tmps3;
        cin >> tmpnum >> tmpname >> tmps1 >> tmps2 >> tmps3;
        if(tmps1 + tmps2 + tmps3 > s){
            num = tmpnum;
            name = tmpname;
            s = tmps1 + tmps2 + tmps3;
        }
    }
    cout << name << " " << num << " " << s;
    return 0;
}
```
