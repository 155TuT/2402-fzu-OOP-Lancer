### 2402 - OOP - 上机1 - Lancer

------

#### 判断题

1. 如果A是B的友元类,那么B的成员函数可以访问A的私有成员。(F)

2. 友元函数或友元类，虽然能够提高的运行效率和编程便捷性，但会对类的封装造成一定程度上的破坏，因此，在使用时应慎重。  (T)

3. 对于类A，若其中的构造函数有A( )和A(int i=0,int y=0)，则在主程序中语句 “A a;”不会出现调用构造函数的二义性，可以正常运行。(F)

4. 设类A中含有指针数据成员，且在对象构造时该指针会指向某块内存区域，类中未重写复制构造函数，则主程序中 “A a；A b(a);”,这两语句执行后，对象a和对象b中的指针会指向不同的内存区域，因为它们是两个独立的对象。(F)

5. 当一个类对象的成员函数被调用时，该成员函数的 this指针指向调用它的对象。(T)
6. 定义了构造函数之后，类不再提供默认的构造函数。(T)
7. 构造函数没有返回值。(T)
8. 关键字struct和class具有相同的功能，struct的默认访问权限是private。(F)
9. 在类内声明某个全局函数为友元函数，它就是类的成员函数。(F)
10. 构造函数的名字与类名完全相同。(T)

------

#### 单选题

1. 如果默认参数的函数声明为`void fun(int a,int b=1,char c='a',float d=3.2);`，则下面调用写法正确的是（B）

   A. fun();

   **B. fun(2,3);**

   C. fun(2, ,'c',3.14);

   D. fun(int a=1);

2. 如有函数定义`void func(int x = 0, int y = 0){ … }`，则下列函数调用中会出现问题的是（A）

   **A. func(1,2, 3);**

   B. func(1,2);

   C. func(1);

   D. func();

3. 以下说法正确的是（C）

   A. 在静态成员函数中可以调用同类的其他任何成员函数

   B. const成员函数不能作用于非const对象

   **C. 在静态成员函数中不能使用this指针**

   D. 静态成员变量每个对象有各自的一份

4. 重载函数在调用时选择的依据中，错误的是（C）

   A. 函数的参数

   B. 参数的类型

   **C. 函数的名字**

   D. 函数的类型

5. 关于数组的叙述，说法错误的是（D）

   A. 对数组的操作，本质上是对数组元素的操作。

   B. 数组的逻辑结构是指在人大脑中的组织结构，一般是以页、行、列的形式出现；而数组的存储结构，是指在内存空间的组织存放形式，一般是是以行的形式存在，数组元素的地址空间是连续的。

   C. 一维数组，其数组名是一个字符常量，为该数组在内存空间的首地址，不允许对其赋值操作。

   **D. 数组作为函数的形参时，其传递方式是采用传址还是传值的方式，由程序员决定。例如 void rowSum(int a[][4], int nRow) 中，很显然在函数调用时，形参数组a将来与实参结合的方式采用的是传值。**

6. 关于函数的重载，下面 4 组重载函数的声明中，（D）是正确的

   A.

   ```c++
   void F();
   char F();
   int F();
   double F();
   ```

   B.

   ```c++
   void F(int a);
   void F(int b);
   void F(int c);
   void F(int d);
   ```

   C.

   ```c++
   void F();
   void F(int x);
   void F(double x);
   void F(int x, int y);
   ```

   **D.**

   ```c++
   void F();
   void F(int x);
   void F(int x, int y);
   void F(int x = 0, int y = 0);
   ```

7. 下面叙述中错误的是（A）

   **A. 主函数中定义的变量在整个程序中都是有效的**

   B. 替换为在其他函数中定义的变量在主函数中也都不能使用

   C. 形式参数也是局部变量

   D. 复合语句中定义的函数只在该复合语句中有效

8. C++语言中若不特别声明，则变量的类型被认为是（C）

   A. extern

   B. static

   **C. register**

   D. auto

9. 对函数的调用不可以出现在（C）

   A. 对一个变量赋初值

   B. 调用函数时传递的实际参数

   **C. 函数的形式参数**

   D. 引用数组元素[ ]的运算符中

10. 在下面的函数声明中，存在着语法错误的是（C）

    A. BC (int a, int) ;

    B. BC (int, int) ;

    **C. BC (int, int=5);**

    D. BC (int x, int y);

11. 下列函数中，（C）不能重载

    A. 成员函数

    B. 非成员函数

    **C. 析构函数**

    D. 构造函数

12. 下列对重载函数的描述中，（A）是错误的

    **A. 重载函数中不允许使用默认参数**

    B. 重载函数中编译根据参数表进行选择

    C. 不要使用重载函数来描述毫无相干的函数

    D. 构造函数重载将会给初始化带来多种方式

13. 设A为自定义类，现有普通函数int fun(A& x)。则在该函数被调用时（C）

    A. 将执行复制构造函数来初始化形参x

    B. 仅在实参为常量时，才会执行复制构造函数以初始化形参x

    **C. 无需初始化形参x**

    D. 仅在该函数为A类的友元函数时，无需初始化形参x

14. 以下说法正确的是（C）

    A. 每个对象内部都有成员函数的实现代码

    B. 一个类的私有成员函数内部不能访问本类的私有成员函数

    **C. 类的成员函数之间可以相互调用**

    D. 编写一个类时，至少要写一个成员函数

15. 以下对类A的定义中正确的是（B）

    A. `class A{private：int v;public : void Func(){}}`

    **B. `class A{private : int v;A *next;};`**

    C. `class A{int v;public:void Func();};A::void Func(){}`

    D. `class A{int v;public: A next;void Func(){ }};`

16. 假如有以下类A：

    ```c++
    classA{
    public：
        int func(int a){return a*a;}
    };
    ```

    以下程序片段中不正确的是（C）

    A. `A a;a.func(5);`

    B. `A*p=new A; p->func(5);`

    **C. `A a;  A& r=a;r.func(5);`**

    D. `A a,b; if(a!=b) a.func(5);`

17. 有关类和对象的说法下列不正确的有（C）

    A. 对象是类的一个实例

    B. 任何一个对象只能属于一个具体的类

    **C. 一个类只能有一个对象**

    D. 类与对象和关系与数据类型和变量的关系相似

18. 在下面类声明中，关于生成对象不正确的是（C）

    ```c++
    class point{
    public:
        int x, y;
        point(int a,int b){x=a;y=b;}
    };
    ```

    A. point p(10,2);

    B. point *p=new    point(1,2);

    **C. point *p=new point[2];**

    D. point *p[2]={new point(1,2), new  point(3,4)};

19. 所有类都应该有（D）

    A. 构造函数

    B. 析构函数

    C. 构造函数和析构函数

    **D. 以上答案都不对**

20. 析构函数可以返回（D）

    A. 指向某个类的指针

    B. 某个类的对象

    C. 状态信息表明对象是否被正确地析构

    **D. 不可返回任何值**

21. 友元的作用是（B）

    A. 提高程序的运用效率

    **B. 加强类的封装性**

    C. 实现数据的隐藏性

    D. 增加成员函数的种类

22. 下列属于类的析构函数特征的是（A）

    **A. 一个类中只能定义一个析构函数**

    B. 析构函数名与类名不同

    C. 析构函数的定义只能在类体内

    D. 析构函数可以有一个或多个参数

23. 如果类定义中没有使用 private、protected、或public 关键字，则所有成员（C）

    A. 都是 public 成员

    B. 都是 proctected 成员

    **C. 都是 private 成员**

    D. 不一定

24. 现有类的定义如下：

    ```c++
    class MyClass {
    public:
        MyClass(int x): val(x) {}
        void Print() const {cout << "const:val=" << val << '\t';}
        void Print() {cout << "val=" << val << '\t';}
    private:
        int val;
    };
    ```

    在main函数中定义该类的l两个对象：const MyClass obj1(10);  MyClass obj2(20);依次执行obj1.Print(); obj2.Print();的输出结果是（C）

    A. `val=10    const:val=20`

    B. `const:val=10   const:val=20`

    **C. `const:val=10 val=20`**

    D. `val=10 val=20`

25. 下面程序的运行结果为（B）

    ```c++
    #include<iostream.h>
    class A
    {
      int num;
    public:
      A（int i）{num=i;}
      A（A &a）{num=a.num++;}
      void print（）{cout<<num;}
    };
    void main（）
    {
      A a （1）,b（a）;
      a.print（）;
      b.print（）;
    }
    ```

    A. 11

    **B. 12**

    C. 21

    D. 22

26. 类的析构函数是在什么时候调用的？（C）

    A. 类创建时

    B. 创建对象时

    **C. 删除对象时**

    D. 不自动调用

27. 关于类的静态数据成员和静态函数成员，说法错误的是（D）

    A. 类的静态数据成员，解决的是同类不同对象之间的数据共享问题。

    B. 类的静态数据成员，具有静态声明周期，必须在命名空间作用域的某个地方对其进行初始化。

    C. 静态成员函数可以直接访问该类的静态数据成员和函数成员；而访问类的非静态成员，必须通过对象名。

    **D. 静态数据成员，属于对象的属性。若要对静态数据成员进行访问，必须通过对象名。**

28. 下列关于this指针的叙述中，正确的是（D）

    A. 任何与类相关的函数都有this指针

    B. 类的成员函数都有this指针

    C. 类的友元函数都有this指针

    **D. 类非静态成员函数才有this指针**

------

#### 填空题

有如下程序：请写出程序输出结果。

```c++
class Test
{
public:
    Test(){cout<<"构造函数"<<endl;}        
    ~Test(){cout<<"析构函数"<<endl;}    
};
void myfunc(){
    static Test obj;
}
int main()
{
    cout<<"main开始"<<endl;
    myfunc();
    cout<<"main结束"<<endl;
    return 0；
}
```

答案：

main开始

构造函数

main结束

析构函数



------

#### 程序填空题

*空的部分在程序中用额外的小括号括起*

1.将空白的地方填写完整，使程序完成指定的功能。

```c++
#include <iostream>
using namespace std;
class Student
 {public:
   (Student(int n, float s) : num(n), score(s) {})//利用参数初始化表进行数据初始化
   void display();
  private:
   int num;
   float score;
 };

void Student::display()
 {cout<<num<<" "<<score<<endl;}
 
int main()
{
  Student stud[5]={
  Student(101,78.5),Student(102,85.5),Student(103,98.5),
  Student(104,100.0),Student(105,95.5)}; //定义对象数组
 (Student *p = stud;)//定义对象指针指向对象数组
 for((int i = 0, p = &stud[i]; i < 5; i += 2))//显示第1、3、5名学生信息
  p->display();
 return 0;
 }
}
```



2.已知平面上的一点由其横纵坐标来标识。本题要求按照已给代码和注释完成一个基本的“点”类的定义（坐标均取整型数值）。并通过主函数中的点类对象完成一些简单操作，分析程序运行结果，将答案写在对应的空格中。

```c++
#include <(iostream)>
using namespace std;

class Point
{
(private:)//访问权限设置，私有权限
    int x;//横坐标
    int y;//纵坐标
(public:)//访问权限设置，公有权限

    //以下为构造函数，用参数a,b分别为横纵坐标进行初始化
    (Point)(int a,int b)
    {
        (x(a));
        (y(b));
    }
    
    //以下为拷贝构造函数，借用对象a_point完成初始化
    Point((const Point& )a_point)
    {
        x=a_point.x;
        y=a_point.y;
    }
    
    //以下为析构函数
    (~Point())
    {
        cout<<"Deconstructed Point";
        print();
    }
    
    //以下为输出点的信息的函数，要求在一行中输出点的坐标信息，形如：(横坐标,纵坐标)
    void print()
    {
        cout<<("(" << x << "," << y << ")")<<endl;
    }
};


int main()
{
    Point b_point(0,0);
    b_point.print();
    int a,b;
    (cin >> a >> b;)//从标准输入流中提取数值给a,b
    Point c_point(a,b);
    c_point.print();
  (return 0;)//主函数的返回语句
}
/*设输入为10 10，则本程序的运行结果为：
((0,0))
((10,10))
(Deconstructed Point(10,10))
(Deconstructed Point(0,0))
*/
```

3.AccountCNY类表示人民币账户，AccountUSD类表示美元账户，账户余额为私有数据成员。a.transfer(b,100)表示从a账户转出100元（a账户币种）至b账户。当a和b账户的币种相同时，a的余额减少100，b的余额增加相同值；当a、b账户币种不同时，a的余额减少100，但b的余额增加值应进行汇率换算。

请将下述代码补充完整，使其能正常运行。假设汇率为1美元兑6.5元人民币。

```c++
#include <iostream>
#include <stdio.h>
using namespace std;

class AccountUSD;
class AccountCNY {
private:
    double dBalance {0};
public:
    void deposit(double fAmount){ //存款函数
        (dBalance += fAmount;)
    }

    double balance(){
        return dBalance;
    }

    bool transfer(AccountCNY& b, double fAmount){
        if (dBalance < fAmount)
            return false;
        dBalance -= fAmount;
        b.dBalance += (fAmount;)
        return  true;
    }

    bool transfer((AccountCNY& b), double fAmount);
    friend (class AccountUSD;)
};

class AccountUSD {
private:
    double dBalance {0};
public:
    void  deposit(double fAmount){
        (dBalance += fAmount;)
    }

    double balance(){
        return dBalance;
    }

    bool transfer(AccountUSD& b, double fAmount){
        if (dBalance < fAmount)
            return false;
        (dBalance -= fAmount;)
        b.dBalance += fAmount;
        return  true;
    }

    bool transfer(AccountCNY& b, double fAmount);
    friend (class AccountCNY)
};

bool AccountCNY::transfer(AccountUSD& b, double fAmount){
    if (dBalance < fAmount)
        return false;
    dBalance -= fAmount;
    b.dBalance += (fAmount / 6.5;)
    return  true;
}

bool AccountUSD::transfer(AccountCNY& b, double fAmount){
    if (dBalance < fAmount)
        return false;
    dBalance 2 分
    b.dBalance += (fAmount * 6.5;)
    return  true;
}

int main()
{
    AccountCNY a, b;
    a.deposit(1000); b.deposit(1000);
    printf("Deposit CNY 1000 to a & b\n");
    printf("CNY Account a: %.2f\n",a.balance());
    printf("CNY Account b: %.2f\n",b.balance());

    AccountUSD c,d;
    c.deposit(1000); d.deposit(1000);
    printf("Deposit USD 1000 to c & d\n");
    printf("USD Account c: %.2f\n",c.balance());
    printf("USD Account d: %.2f\n",d.balance());

    a.transfer(b,100);
    printf("Transfer CNY 100 from a --> b\n");
    printf("CNY Account a: %.2f\n",a.balance());
    printf("CNY Account b: %.2f\n",b.balance());

    c.transfer(d,100);
    printf("Transfer USD 100 from c --> d\n");
    printf("USD Account c: %.2f\n",c.balance());
    printf("USD Account d: %.2f\n",d.balance());

    a.transfer(d,650);
    printf("Transfer CNY 650 from a --> d\n");
    printf("CNY Account a: %.2f\n",a.balance());
    printf("USD Account d: %.2f\n",d.balance());

    c.transfer(a,100);
    printf("Transfer USD 100 from c --> a\n");
    printf("USD Account c: %.2f\n",c.balance());
    printf("CNY Account a: %.2f\n",a.balance());

    return 0;
}
```





------

#### 函数题

##### 1.我自己写字符串类（基础版）

完成`MyString`类的实现，使程序正确运行

**裁判测试程序样例：**

```c++
#include <iostream>
#include <cstring>
using namespace std;

class MyString {
public:
    // 无参构造函数
    // 空字符串可以考虑使用new char[1]，并设置字符串结束符
    MyString();
    // 构造函数，传入一个C语言风格字符串
    MyString(const char *s);
    // 拷贝构造函数
    MyString(const MyString &s);
    // 析构函数
    ~MyString();
    // 返回子串 [pos, pos+count)
    // 若pos不在字符串的下标范围内，返回空的MyString对象
    // 若请求的子串越过字符串的结尾，即count大于size() - pos，则返回的子串为[pos, size()) 
    // 若count == -1，返回子串[pos, size())
    // 可以考虑使用strncpy
    MyString substr(int pos = 0, int count = -1);
    // 返回下标为pos的字符的引用
    char& at(int pos);
    // 字符串的长度
    int size();
    // 返回C语言风格的字符串
    const char* c_str();
private:
    char *m_buf;
    int m_size;
};

// 请将答案填写在这里

int main() {
    char s[101];
    cin.getline(s, 101);
    int pos, count;
    cin >> pos >> count;
    // 创建、拷贝、空字符串
    MyString s1(s), s2(s1), s3;
    s1.at(0) = 'x';
    s2.at(0) = 'X';
    cout << "s1: " << s1.c_str() << endl;
    cout << "s2: " << s2.c_str() << endl;
    cout << "s3: " << s3.c_str() << endl;
    // 取子串
    cout << "substr: " << s2.substr(pos, count).c_str() << endl;
    // 以后还可以直接使用<<输出一个MyString对象哦 TODO
    // cout << s1 << endl;
    return 0;
}
```

**输入样例：**

第一行：输入字符串，长度最大为100
第二行：取子串时的下标和长度

```in
abcdefg
0 3
```

**输出样例：**

在这里给出相应的输出。例如：

```out
s1: xbcdefg
s2: Xbcdefg
s3: 
substr: Xbc
```

**code:**

```c++
MyString::MyString() : m_buf(new char[1]), m_size(0){
    m_buf[0] = '\0';
}
MyString::MyString(const char *s){
    m_size = strlen(s);
    m_buf = new char[m_size + 1];
    strcpy(m_buf, s);
}
MyString::MyString(const MyString &s){
    m_size = s.m_size;
    m_buf = new char[m_size + 1];
    strcpy(m_buf, s.m_buf);
}

MyString::~MyString(){
    delete[] m_buf;
}
MyString MyString::substr(int pos, int count){
    if (pos < 0 || pos >= m_size) return MyString();
    int available = m_size - pos;
    int actual_count = (count == -1) ? available : std::min(count, available);
    char* temp = new char[actual_count + 1];
    strncpy(temp, m_buf + pos, actual_count);
    temp[actual_count] = '\0';
    MyString result(temp);
    delete[] temp;
    return result;
}
char& MyString::at(int pos){
    return m_buf[pos];
}
int MyString::size(){
    return m_size;
}
const char* MyString::c_str(){
    return m_buf;
}
```

##### 2.计算两点间距离（友元函数）

现有一个类Point表示二维空间中的点，包含私有数据成员double x和double y，x表示该点的x坐标，y表示该点的y坐标。要求编写一个友元函数，输出两点之间的距离。
输入说明：
      每一行四个数值，前两个数是第一个坐标点的x坐标和y坐标，后两个数是第二个坐标点的x坐标和y坐标。当输入四个0时表示输入结束。
输出说明：
     输出两点距离必须保留两位小数。

**函数接口定义:**

```c++
//输出两个点p1和p2之间的距离，要求输出结果必须保留两位小数。
void pointDis（Point& p1, Point& p2）;
```

其中`p1` 和 `p2` 都是用户传入的参数。函数须计算p1和p2的距离并输出，要求输出结果必须保留两位小数。

**裁判测试程序样例:**

```c

#include<iostream>
#include<cmath>
#include<iomanip>
using namespace std;
class Point {
    public:
        Point() {
        }
        Point(double px,double py) {
            x=px;
            y=py;
        }
        friend void pointDis(Point &p1,Point &p2);
    private:
        double x;
        double y;
};
/* 请在这里填写答案 */

int main() {
    double x1,y1,x2,y2;
    cin>>x1>>y1>>x2>>y2;
    Point p1,p2;
    while(!(x1==0&&y1==0&&x2==0&&y2==0)) {
        p1=Point(x1,y1);
        p2=Point(x2,y2);
        pointDis(p1,p2);
        cin>>x1>>y1>>x2>>y2;
    }
    return 0;
}


```

**输入样例:**

```in
1.5  3.8  4.2  8.5
1  3  4  7
0  0  0  0
```

**输出样例:**

```out
5.42
5.00
```

**code:**

```c++
void pointDis(Point& p1, Point& p2){
    cout << fixed << setprecision(2) << sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y)) << endl;
}
```

##### 3.定义Date类

本题要求实现一个日期类定义，根据所定义的类可以完成相关的类测试。

**Date类定义：**

根据Date被使用的情况，进行Date类定义，要求通过构造函数进行日期初始化，并通过display（）函数进行日期格式显示，显示格式为"月/日/年"

**测试程序样例：**

main( ) 函数定义如下

```c++
int main()
{
 Date d1(3,25,2019);
 Date d2(3,30);
 Date d3(10);
 Date d4;
 d1.display();
 d2.display();
 d3.display();
 d4.display();
 return 0;
 }

/* 请在这里填写答案 */
```

**输出样例：**

在这里给出相应的输出。例如：

```out
3/25/2019
3/30/2019
10/1/2019
1/1/2019
```

**code:**

```c++
#include <iostream>
using namespace std;

class Date{
private:
    int month, day, year;
    static int default_month;
    static int default_day;
    static int default_year;
public:
    Date(int m, int d, int y) : month(m), day(d), year(y) {}
    Date(int m, int d) : month(m), day(d), year(default_year) {}
    Date(int m) : month(m), day(default_day), year(default_year) {}
    Date() : month(default_month), day(default_day), year(default_year) {}
    void display() {
        cout << month << "/" << day << "/" << year << endl;
    }
};

int Date::default_month = 1;    // 默认月为1
int Date::default_day = 1;      // 默认日为1
int Date::default_year = 2019;  // 默认年为2019
```



------

#### 编程题

##### 1.用函数求两个整数的最大公约数和最小公倍数

编写两个函数，分别求两个整数的最大公约数和最小公倍数，并用主函数调用这两个函数，然后输出结果。两个整数由键盘输入。约定最大公约数为正整数

**输入格式:**

输入均不为0的整数n和m(n与m的乘积还在整数范围内)

**输出格式:**

输出这两个整数的最大公约数和最小公倍数

**输入样例:**

```in
24 36
-48 128
```

**输出样例:**

```out
12 72
16 -384
```

\###提示

公约数、公倍数

提示：a,b里有负的则最小公倍数就为负的

**code:**

```c++
#include <iostream>
#include <cmath>

int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

int lcm(int a, int b) {
    using std::abs;
    int sgn = 1;
    if(a < 0 || b < 0){
        sgn = -1;
    }
    return sgn * abs(a) / gcd(abs(a), abs(b)) * abs(b);
}

int main() {
    int n, m;
    while (std::cin >> n >> m) {
        int g = gcd(std::abs(n), std::abs(m));
        int l = lcm(n, m);
        std::cout << g << " " << l << std::endl;
    }
    return 0;
}
```

##### 2.宿舍谁最高

学校选拔篮球队员，每间宿舍最多有 4 个人。现给出宿舍列表，请找出每个宿舍最高的同学。定义一个学生类 Student，有身高 height，体重 weight 等。

**输入格式:**

首先输入一个整型数 *n* （1≤*n*≤106），表示有 *n* 位同学。 

紧跟着 *n* 行输入，每一行格式为：`宿舍号 name height weight`。
`宿舍号`的区间为 [0, 999999]， `name` 由字母组成，长度小于 16，`height`，`weight` 为正整数。  

**输出格式:**

按宿舍号从小到大排序，输出每间宿舍身高最高的同学信息。题目保证每间宿舍只有一位身高最高的同学。

注意宿舍号不足 6 位的，要按 6 位补齐前导 0。

**输入样例:**

```in
7
000000 Tom 175 120
000001 Jack 180 130
000001 Hale 160 140
000000 Marry 160 120
000000 Jerry 165 110
000003 ETAF 183 145
000001 Mickey 170 115
```

**输出样例:**

```out
000000 Tom 175 120
000001 Jack 180 130
000003 ETAF 183 145
```

**code:**

```c++
#include <iostream>
#include <unordered_map>
#include <vector>
#include <string>
#include <iomanip>
#include <algorithm>
using namespace std;
struct Student{
    int dorm, height, weight;
    string name;
};
int main(){
    int n;
    cin >> n;
    unordered_map<int, Student> dormMax;
    for(int i = 0; i < n; i++){
        int dorm, h, w; string name;
        cin >> dorm >> name >> h >> w;
        if(dormMax.find(dorm) == dormMax.end()){
            dormMax[dorm] = {dorm, h, w, name};
        }else if(h > dormMax[dorm].height){
            dormMax[dorm] = {dorm, h, w, name};
        }
    }
    vector<Student> res;
    for(auto &item : dormMax){
        res.push_back(item.second);
    }
    sort(res.begin(), res.end(), [](const Student &a, const Student &b){ return a.dorm < b.dorm; });
    for(auto &s : res){
        cout << setw(6) << setfill('0') << s.dorm << " " << s.name << " " << s.height << " " << s.weight << "\n";
    }
    return 0;
}
```

##### 3.求两点之间距离

定义一个Point类，有两个数据成员：x和y, 分别代表x坐标和y坐标，并有若干成员函数。
定义一个函数Distance(), 用于求两点之间的距离。

**输入格式:**

输入有两行：
第一行是第一个点的x坐标和y坐标；
第二行是第二个点的x坐标和y坐标。

**输出格式:**

输出两个点之间的距离，保留两位小数。

**输入样例:**

```in
0 9
3 -4
```

**输出样例:**

```out
13.34
```

**code:**

```c++
#include <iostream>
#include <cmath>
#include <iomanip>
class Point{
private:
    double x, y;
public:
    Point(double x = 0.0, double y = 0.0) : x(x), y(y) {}
    ~Point() {}
    friend double Distance(const Point& p1, const Point& p2);
};
double Distance(const Point& p1, const Point& p2){
    return std::sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y));
}

int main(){
    double x1, y1, x2, y2;
    std::cin >> x1 >> y1 >> x2 >> y2;
    Point* p1 = new Point(x1, y1);
    Point* p2 = new Point(x2, y2);
    std::cout << std::fixed << std::setprecision(2) << Distance(*p1, *p2);
    delete p1;
    delete p2;
    return 0;
}
```

##### 4.复数类的操作

1、声明一个复数类Complex（类私有数据成员为double型的real和image） 

2、定义构造函数，用于指定复数的实部与虚部。

3、定义取反成员函数，调用时能返回该复数的相反数（实部、虚部分别是原数的相反数）。 

4、定义成员函数Print()，调用该函数时，以格式(real, image)输出当前对象。

5、编写加法友元函数，以复数对象c1，c2为参数，求两个复数对象相加之和。 

6、主程序实现： 

（1）读入两个实数，用于初始化对象c1。 

（2）读入两个实数，用于初始化对象c2。 

（3）计算c1与c2相加结果，并输出。 

（4）计算c2的相反数与c1相加结果，并输出。

**输入格式:**

输入有两行： 

第一行是复数c1的实部与虚部，以空格分隔； 

第二行是复数c2的实部与虚部，以空格分隔。

**输出格式:**

输出共三行: 

第一行是c1与c2之和；

第二行是c2的相反数与c1之和；

第三行是c2 。

**输入样例:**

在这里给出一组输入。例如：

```in
2.5 3.7
4.2 6.5
```

**输出样例:**

在这里给出相应的输出。例如：

```out
(6.7, 10.2)
(-1.7, -2.8)
(4.2, 6.5)
```

**code:**

```c++
#include <iostream>
using namespace std;
class Complex{
private:
    double real;
    double image;
public:
    Complex(double r = 0.0, double i = 0.0) : real(r), image(i) {}
    ~Complex() {}
    Complex Negate() const {
        return Complex(-real, -image);
    }
    void Print() const {
        cout << "(" << real << ", " << image << ")" << endl;
    }
    friend Complex Add(const Complex& c1, const Complex& c2);
};
Complex Add(const Complex& c1, const Complex& c2){
    return Complex(c1.real + c2.real, c1.image + c2.image);
}
int main(){
    double r1, i1, r2, i2;
    cin >> r1 >> i1;
    Complex c1(r1, i1);
    cin >> r2 >> i2;
    Complex c2(r2, i2);
    Complex sum = Add(c1, c2);
    sum.Print();
    Complex negSum = Add(c2.Negate(), c1);
    negSum.Print();
    c2.Print();
    return 0;
}
```

