---
link: https://pintia.cn/problem-sets/1912505000558997504/exam/problems/type/1
---
### 2402 - OOP - 上机3 - Lancer

------

#### 判断题

1. 如果在一个文件中声明了 using namespace A; 和 using namespace B;，而命名空间A和B中都有一个相同名字的函数 func()，那么简单调用 func() 将会产生编译错误，因为编译器不知道使用哪个命名空间的函数。(T)
2. 在C++中，可以使用`getline()`函数从`cin`对象中读取一整行文本，包括空格。(T)
3. 可以使用任何类型的对象作为 **`throw`** 表达式的操作数。(T)
4. 在 C++ 中，将派生类的指针直接赋值给基类的指针是不允许的，需要进行显式类型转换。(F)
5. 抽象类可以被直接实例化，但是它的纯虚函数必须在派生类中被重写。(F)
6. 在 C++ 中，如果函数参数是包含大量数据成员的类对象，为了提高空间效率，应考虑使用引用传递而非值传递。(T)
7. 如果A是B的友元类,那么B的成员函数可以访问A的私有成员。(F)
8. （2024Final）在C++中，链表节点的内存空间是连续分配的。(F)
9. 在 C++ 中的多层继承结构中，最底层的派生类在构造过程中需要显式调用其所有直接以及间接基类的构造函数。(F)
10. 成员函数形式的运算符重载不需要通过对象来调用。(F)

------

#### 单选题

1. C ++中对">>"运算符重载，重载函数必须是一个(  )。（C）

   A. 用于输出操作的非成员函数

   B. 用于输出操作的成员函数

   **C. 用于输入操作的非成员函数**

   D. 用于输入操作的成员函数

2. 常对象的特点不包括：（D）

   A. 不能修改成员变量

   B. 可以调用常成员函数

   C. 不能调用非常成员函数

   **D. 不能被复制**

3. 在C++中，this指针的主要用途是什么？（B）

   A. 指向当前对象的成员函数

   **B. 指向当前对象**

   C. 在成员函数内部访问类的静态成员

   D. 调用其他对象的成员函数

4. 在C++中，以下哪个声明表示类A是类B的友元？(  )（B）

   A. class A friend; 在B内部

   **B. friend class A; 在B内部**

   C. class B friend; 在A内部

   D. friend class B; 在A和B内部都需要声明

5. 如果一个异常在try块中被抛出，但没有被相应的catch块捕获，会发生什么？（A）

   **A. 程序会调用std::terminate()**

   B. 异常会被忽略

   C. 程序会尝试重新抛出异常

   D. 程序会继续执行下一个try块

6. 在 C++ 类体系中，以下哪些特殊成员函数不能被派生类继承？（D）

   A. 构造函数

   B. 析构函数

   C. 复制构造函数

   **D. 所有上述选项**

7. 下列哪个C++风格的语句可以打开一个名为"example.txt"的文件以进行写入操作（ ）。（B）

   A. ifstream file("example.txt");

   **B. ofstream file("example.txt");**

   C. fstream file("example.txt", ios::in);

   D. freopen("example.txt", "w", stdout);

8. 在 C++ 中，下列关于静态成员函数的描述中，不正确的是：（B）

   A. 静态成员函数可以通过类名直接调用。

   **B. 静态成员函数可以访问类的非静态成员。**

   C. 静态成员函数不依赖于类的任何实例。

   D. 静态成员函数不能被声明为虚函数。

9. 如果一个函数模板和一个普通函数都适用于某个函数调用，那么（    ）。（B）

   A. 编译器会报错

   **B. 普通函数会被调用**

   C. 函数模板会被调用

   D. 结果是未定义的

10. 在C++中，关于对象数组，以下哪个说法是正确的？（D）

   A. 对象数组只能存储基本数据类型，不能存储类的对象。

   B. 对象数组的所有元素都共享相同的内存地址。

   C. 对象数组的每个元素都是类的静态成员。

   **D. 对象数组的每个元素都是类的不同实例。**


------

#### 程序填空题

1.CAT's Copy

阅读下面的程序，完成其中复制构造函数的代码。

```C++
#include <iostream>
using namespace std;
class CAT
{     public:
           CAT();
           CAT(const CAT&);
          ~CAT();
          int GetAge() const { return *itsAge; }
          void SetAge(int age){ *itsAge=age; }
      protected:
          int* itsAge;
};
CAT::CAT()
{    itsAge=new int;
     *itsAge =5;
}
CAT::CAT(const CAT& c)
{
/*（itsAge = new int）（5分）*/;
/*（*itsAge = *(c.itsAge)）（5分）*/;
}
CAT::~CAT()
{     delete itsAge;   }
```

2.静态数据成员

填写程序中的空白，完成指定的功能

```c++
#include<iostream>
using namespace std;
class Point{
    double x,y;
    /*（static int cnt;）（2分）*///定义静态变量
public:
    Point(double a=0,double b=0):x(a),y(b){
        /*（cnt++;）（2分）*/
    }
    ~Point(){
        /*（cnt--;）（2分）*/
    }
    void show(){
        cout<<"the number of Point is "<</*（cnt）（2分）*/<<endl;
    }
};
/*（int Point::cnt = 0;）（2分）*/
int main(){
    Point p1;
    Point *p=new Point(1,2);
    p->show();
    delete p;
    p1.show();
    return 0;
```
####程序输出如下：
```
the number of Point is 2
the number of Point is 1
```

3.（2024Final）餐厅类的构造函数

在本题中，考生需要设计一个模拟餐厅的系统。餐厅作为一个特殊的建筑物（`Building` 类的派生类），包含名字、位置信息并包括一个管理者（`Manager`类的对象）。请完善以下程序：

```c++
#include <iostream>
#include <string>
using namespace std;

// 基类 Building
class Building {
public:
    Building(string loc) /*（: location(loc)）（3分）*///为类成员提供初始化
    {
        cout << "Building located at: " << location << endl;
    }
    string location;
};

// 独立类 Manager
class Manager {
public:
    Manager(int id, string nam) /*（: emp_id(id), name(nam)）（3分）*/ //为类成员提供初始化
    {}
    void display() {
        cout << "Employee ID: " << emp_id << endl << "Name: " << name << endl;
    }
private:
    int emp_id;
    string name;
};

// 派生类 Restaurant
class Restaurant /*（: public Building）（3分）*/  //选择合适的方式继承Building
{
public:
    // Restaurant构造函数需要初始化Building的构造函数
    Restaurant(string loc, string name, int m_id, string m_name)
    /*（: Building(loc), manager(m_id, m_name), restaurant_name(name)）（3分）*/ //为类成员初始化，注:name是restaurant的名字，m_name是经理的名字
    {
        restaurant_name = name;
        cout << "Restaurant " << restaurant_name << " is now open." << endl;
    }
    void show() {
        cout << "Restaurant details:" << endl;
        cout << "Location: " << /*（location）（3分）*/ << endl; //使用继承自父类的location成员
        cout << "Manager details:" << endl;
        manager.display();
    }
private:
    Manager manager;
    string restaurant_name;
};

int main() {
  string location, restaurantName, managerName;
  int managerID;
  getline(cin, location);
  getline(cin, restaurantName);
  getline(cin, managerName);
  cin >> managerID;
  Restaurant restaurant(location, restaurantName, managerID, managerName);
  restaurant.show();
  cout << "Location Check: " << restaurant.location << endl;
  return 0;
}
```


------

#### 函数题

##### 1.（2024Final）学生考勤管理程序（链表）

题目描述：
假设你正在开发一个学生考勤管理程序，需要实现一些功能来处理学生的考勤情况。你决定使用链表来记录学生的考勤。每个学生有一个唯一的学号（无重复），考勤情况包括出勤（attend）、迟到 (late)、旷课 (absent) 三类。本程序能够实现以下功能：
1\. 输入一系列 <学号-出勤状态> 信息，以-1为结尾；
2\. 根据以上输入，新建一个存储学生考勤情况信息的链表；
3\. 继续输入某一种感兴趣的出勤状态，比如“attend”，统计并输出该状态下的学生人数；
4\. 将链表中为“late”状态的所有节点删除，输出执行删除操作后的链表。


节点结构定义如下：
```
struct Node {
int studentID;
string attendanceStatus;
Node* next;
Node(int id, string status) : studentID(id), attendanceStatus(status), next(NULL) {}
};
```
\
请根据以上描述以及裁判测试程序，实现以下三个功能函数：
```C++
Node* addStudent(Node* head, int id, string status)； // 将一个新的学生节点添加到链表中，包括学号 id 和考勤情况 status。函数应返回更新后的链表头节点。
int countAttendance(Node* head, string status); // 统计特定考勤状态下的学生数量。接受链表中的头节点 head 以及要统计的考勤状态 status，返回具有特定考勤状态的学生数量。
void removeAllLatecomers(Node* &head); // 移除所有迟到的学生节点。接受链表中的头节点的引用 head，在原链表上直接进行修改。
```

裁判测试程序样例：
```c++
#include
#include
using namespace std;
// 节点结构定义
struct Node {
int studentID;
string attendanceStatus;
Node* next;
Node(int id, string status) : studentID(id), attendanceStatus(status), next(NULL) {}
};
// 三个函数实现在这里，请答题者补充完整。
int main() {
Node* head = NULL;
int studentID;
string status;
// 添加学生信息（学号 出勤状态）
cout << "Please input student No. and status (for example: 1 late)" << endl;
cout << "input -1 for ending." << endl;
while (true) {
cin >> studentID;
if (studentID == -1) {
break;
}
cin >> status;
head = addStudent(head, studentID, status);
}
// 统计特定考勤状态下的学生数量
string searchStatus;
cout << "Please input interested status for counting. (attend/late/absent)" << endl;
cin >> searchStatus;
cout << "The number of " << searchStatus << " student is " << countAttendance(head, searchStatus) << endl;
// 移除所有迟到的学生节点
removeAllLatecomers(head);
// 输出移除所有迟到的学生节点后的链表
cout << "The list after deleting late students:" << endl;
Node* current = head;
while (current != NULL) {
cout << current->studentID << " " << current->attendanceStatus << endl;
current = current->next;
}
return 0;
}
```
**输入样例：**
在这里给出一组输入。例如：
```in
1 absent
2 attend
3 late
-1
late
```
**输出样例：**
在这里给出相应的输出。例如：
```out
Please input student No. and status (for example: 1 late)
input -1 for ending.
Please input interested status for counting. (attend/late/absent)
The number of late student is 1
The list after deleting late students:
1 absent
2 attend
```

**code:**

```c++
Node* addStudent(Node* head, int id, string status){
    Node* tmpNode = new Node(id, status);
    if(head == NULL) return tmpNode;
    Node* now = head;
    while(now->next != NULL) now = now->next;
    now->next = tmpNode;
    return head;
}

int countAttendance(Node* head, string status){
    int cnt = 0;
    Node* now = head;
    while(now != NULL){
        cnt += (now->attendanceStatus == status);
        now = now->next;
    }
    return cnt;
}

void removeAllLatecomers(Node* &head){
    Node* now = head;
    Node* prev = NULL;
    while (now != NULL) {
        if (now->attendanceStatus == "late") {
            if (prev == NULL) {
                head = now->next;
                delete now;
                now = head;
            } else {
                prev->next = now->next;
                delete now;
                now = prev->next;
            }
        } else {
            prev = now;
            now = now->next;
        }
    }
}
```

##### 2.（2024Final）有序插入函数

Insert函数模板用于实现有序数组A中元素的有序插入操作，数组A是模板类ordered_array的实例类，最大容量为maxsize，当前已经存储元素个数为size，若插入操作时，数组已满，则数组中不再存储包含新插入元素在内的所有元素中的最小元素。
可适用于各种有序数据类型，例如char、int、double、float、string等。
主函数用于将测试各种有序数据类型下数组的插入操作，形成最终的有序数组，并输出。
请完成Insert函数模板的具体实现。
函数接口定义：
```c++
void insert(ordered_array & A, T item);
```
其中 `A` 是根据实际有序数据类型创建的ordered_array实例类。 `item` 是输入的当前插入元素。
**裁判测试程序样例：**
```c++
#include
#include
using namespace std;
template
class ordered_array
{
public:
T * table;
int size;
int maxsize;
ordered_array(int len)
{
table=new T[len];
maxsize=len;
size=0;
}
~ordered_array(){delete [] table;}
};
/* 请在这里填写答案 */
template
void input(ordered_array & A)//用于从输入中读入元素，并挨个插入有序数组A
{
int length;
cin>>length;
for (int i=0; i>item;
insert(A, item);
}
return;
}
template
void output(ordered_array & A)//用于挨个输出有序数组A的元素
{
for (int i=0; i>num;
switch (i)
{
case 1:{ordered_array int_array(num); input(int_array); output(int_array); break;}
case 2:{ordered_array double_array(num); input(double_array); output(double_array); break;}
case 3:{ordered_array float_array(num); input(float_array); output(float_array); break;}
case 4:{ordered_array char_array(num); input(char_array); output(char_array); break;}
case 5:{ordered_array string_array(num); input(string_array); output(string_array); break;}
}
}
return 0;
}
```
**输入样例：**
共5行，每一行测试int，double，float，char，string五种数据类型。
每一行的第一个数字代表数组初始化大小，第二个数字代表后续输入的元素个数，后面给出具体元素
```in
5 4 2 6 3 7
5 5 3.5 6.7 4.2 7 0.3
5 6 3.2 4.5 3.7 8 9 4.5
4 5 B C D E A
5 7 FZ BJ SH GZ SZ WH HZ
```
**输出样例：**
每一行输出一个有序数组的所有元素。
```out
2 3 6 7
0.3 3.5 4.2 6.7 7
3.7 4.5 4.5 8 9
B C D E
GZ HZ SH SZ WH
```

**code:**

```c++
#include <vector>
#include <algorithm>
template <class T>
void insert(ordered_array<T> & A, T item){
    if(A.size < A.maxsize){
        int pos = A.size;
        for(int i = 0; i < A.size; i++){
            if(A.table[i] > item){
                pos = i;
                break;
            }
        }
        for(int j = A.size; j > pos; j--)A.table[j] = A.table[j - 1];
        A.table[pos] = item;
        A.size++;
    }else{
        vector<T> temp(A.table, A.table + A.size);
        temp.push_back(item);
        sort(temp.begin(), temp.end());
        T min_val = temp[0];
        auto it = find(temp.begin(), temp.end(), min_val);
        if (it != temp.end()) temp.erase(it);
        A.size = 0;
        for(int i = 0; i < temp.size() && A.size < A.maxsize; i++)A.table[A.size++] = temp[i];
    }
}
```

##### 3.狗的继承

完成两个类，一个类Animal，表示动物类，有一个成员表示年龄。一个类Dog，继承自Animal，有一个新的数据成员表示颜色，合理设计这两个类，使得测试程序可以运行并得到正确的结果。

**函数接口定义：**

按照要求实现类

**裁判测试程序样例：**
```c++
/* 请在这里填写答案 */

int main(){
	Animal ani(5);
	cout<<"age of ani:"<<ani.getAge()<<endl;
	Dog dog(5,"black");
	cout<<"infor of dog:"<<endl;
	dog.showInfor();
}

```

**输入样例：**
无

**输出样例：**

```out
age of ani:5
infor of dog:
age:5
color:black

```

**code:**

```c++
#include <iostream>
#include <string>
using namespace std;

class Animal{
protected:
    int age;
public:
    Animal(int a) : age(a){};
    int getAge() const {return age;}
};

class Dog : public Animal{
private:
    string color;
public:
    Dog(int a, string c) : Animal(a), color(c) {}
    void showInfor() const {cout << "age:" << age << endl << "color:" << color << endl;}
};
```


------

#### 编程题

##### 1.（2024Final）图书馆管理程序

**题目描述**

编辑

设计一个简单的图书借阅程序，图书信息由“id + 书名”表示。该程序有以下功能：

向图书馆添加书籍； 借阅书籍； 归还书籍。

假设最多有20本书，每种书只有1本。你需要使用C++编写一个程序，实现以上功能。

提示：1）创建Book类，能够存储书籍对象信息，设置书籍状态等；2）创建图书馆类，以Book类的数组作为私有成员数据，能够添加书籍、完成借书、还书等操作。

请确保代码结构清晰简洁。

**输入格式:**

第一行输入一个整数n，表示要添加到图书馆的书籍数量。

接下来n行，每行包含 书籍ID(一个整数)， 书籍标题（一个字符串），书籍归还状态（0表示未借出，1表示已借出），用空格分隔。

接下来的若干行是操作指令，仅有两种操作（1 借书，2 还书）。比如：

"1 id-1" 表示借阅ID为id-1的书籍。

"2 id-2" 表示归还ID为id-2的书籍。

"0" 表示结束操作。

**输出格式:**

对于每个借阅或归还操作，输出一行描述操作结果。

假设要借ID为1的图书，而该书未被借出，则输出

“Book with ID 1 has been borrowed.”

若该书已经被借走了，则输出：

“Book with ID 3 has already been borrowed.”

若要归还ID为1的书，则输出：

“Book with ID 1 has been returned.”

若要归还的书实际是未被借出的，则输出：

“Book with ID 1 has not been borrowed.”

**输入样例:**

```in
3
1 Introduction_to_Programming 0
2 Data_Structures_and_Algorithms 0
3 Design_Patterns 1
1 1
1 3
2 1
2 1
0
```

**输出样例:**

```out
Book with ID 1 has been borrowed.
Book with ID 3 has already been borrowed.
Book with ID 1 has been returned.
Book with ID 1 has not been borrowed.
```

**code:**

```c++
#include <iostream>
#include <vector>
using namespace std;
class Book{
private:
    int id;
    string title;
    bool in;
public:
    void setId(int _id) {id = _id;}
    void setTitle(string _title) {title = _title;}
    void setIn(bool _in) {in = _in;}
    int getId(){return id;}
    string getTitle(){return title;}
    bool getIn(){return in;}
};

int main(){
    int n;
    cin >> n;
    vector<Book> book(n);
    for(int i = 0; i < n; i++){
        int id;
        string title;
        bool in;
        cin >> id >> title >> in;
        book[i].setId(id);
        book[i].setTitle(title);
        book[i].setIn(in);
    }
    int p;
    cin >> p;
    while(p != 0){
        int id;
        cin >> id;
        if(p - 1){
            for(int i = 0; i < n; i++){
                if(book[i].getId() == id){
                    if(book[i].getIn()){
                        book[i].setIn(0);
                        cout << "Book with ID "<< book[i].getId() <<" has been returned." << endl;
                    } else cout << "Book with ID "<< book[i].getId() <<" has not been borrowed." << endl;
                }
            }
        } else {
            for(int i = 0; i < n; i++){
                if(book[i].getId() == id){
                    if(!book[i].getIn()){
                        book[i].setIn(1);
                        cout << "Book with ID "<< book[i].getId() <<" has been borrowed." << endl;
                    } else cout << "Book with ID "<< book[i].getId() <<" has already been borrowed." << endl;
                }
            }
        }
        cin >> p;
    }
    return 0;
}
```

##### 2.（2024Final）运算符重载

请定义一个分数类，拥有两个整数的私有数据成员，分别表示分子和分母（分母永远为正数，符号通过分子表示）。重载运算符减号"-"，实现两个分数的相减，所得结果必须是最简分数。

**输入格式:**

第一行的两个数 分别表示第一个分数的分子和分母（分母不为0）。 第二行的两个数分别表示 第二个分数的分子和分母（分母不为0）。

**输出格式:**

第一个数表示分子，第二个数表示分母（若分数代表的是整数，则不输出分母）。

**输入样例:**

在这里给出一组输入。例如：

```in
3 5
2 5
```

**输出样例:**

在这里给出相应的输出。例如：

```out
1 5

```

**code:**

```c++
#include <iostream>
#include <stdexcept>
using namespace std;
class Fraction {
private:
    int numerator;
    int denominator;
    static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
public:
    Fraction(int num, int den) : numerator(num), denominator(den) {
        if (denominator == 0) throw invalid_argument("Denominator cannot be zero.");
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
        int common = gcd(abs(numerator), denominator);
        numerator /= common;
        denominator /= common;
    }
    Fraction operator-(const Fraction& other) const {
        int new_num = numerator * other.denominator - other.numerator * denominator;
        int new_den = denominator * other.denominator;
        return Fraction(new_num, new_den);
    }
    int getNumerator() const { return numerator; }
    int getDenominator() const { return denominator; }
};
int main() {
    int num1, den1, num2, den2;
    cin >> num1 >> den1;
    cin >> num2 >> den2;
    try {
        Fraction f1(num1, den1);
        Fraction f2(num2, den2);
        Fraction result = f1 - f2;
        if (result.getDenominator() == 1) cout << result.getNumerator() << endl;
        else cout << result.getNumerator() << " " << result.getDenominator() << endl;
    } catch (const invalid_argument& e) {
        cerr << e.what() << endl;
    }
    return 0;
}
```

##### 3.（2024Final）车辆保费计算

Jerry是PA保险公司的保险经纪，每天需要为不同车辆计算保费，不同车型的保费计算不尽相同。
所有车辆的基本保费由车辆的购车价和车龄决定，购车价*(1-0.05*车龄)*0.1
所有电动车的基本保费需要上浮50%。
除基本保费外，货车的附加保费由车辆载重决定，每吨载重保费500元，一般货车载重缺省为2吨，客车的附加保费由车辆载客数决定，每载客人次保费200元，一般客车载客缺省为5人，电动车还有一笔附加保费由电池容量决定，每度电保费10元。
最终根据是否续保车辆和是否有车辆违章决定保费折扣，续保车辆保费整体享受5%的折扣，但如果车辆有违章则保费整体上浮5%。
现有基类——车辆类Vehicle，包含以下数据成员
`string ID;//车牌`
`int vehicle_price;//车价`
`int vehicle_age;//车龄`
`double premium;//保费`
`double discount;//折扣率`
`bool is_renewal;//是否续保`
`bool has_violation;//有无违章`
电车类EV是车辆类Vehicle的派生类，增加了电池容量的数据成员
`int energy;`
货车Truck类是车辆类Vehicle的派生类，增加了载重量的数据成员
`int weight;`
客车Car类是车辆类Vehicle的派生类，增加了载客人数的数据成员
`int pass_num;`
电动货车E_Truck类是从货车类Truck，电车类EV多重继承而来。
电动客车E_Car类则是从客车类Car，电车类EV多重继承而来。
所有基类和派车类都支持不同的保费计算方法calc_premium()。
现有一个指向Vehicle类对象的指针数组，用于处理输入的各种车型的车辆信息，并根据具体车辆信息计算所有车辆的折扣率和最终保费，并输出。
**输入格式:**
第一行的数字为待输入的车辆数目N。
接下来的N行给出每辆车的基本信息，车牌号，车辆类型，购车价（以万元为单位），车龄，车辆类型分别是T为货车，C为客车，t为电动货车，c为电动客车，电动货车和电动客车还会输入电池容量。
接下来的若干行用于说明续保车辆、违章车辆、载重和载客情况。
每行的第一个字母代表本行的信息类型。
R代表本行所列均为续保车辆，后面跟着若干车牌号，以0作为结束。
V代表本行所列均为违章车辆，后面跟着若干车牌号，以0作为结束。
W代表本行所列货车与电动货车载重量非缺省，后面跟着若干组数据，每两个数据为一组，包含一个车牌和载重量，以0作为结束。
P代表本行所列客车与电动客车载客数非缺省，后面跟着若干组数据，每两个数据为一组，包含一个车牌和载客数，以0作为结束。
E代表所有输入结束。
**输出格式:**
按照车辆基本信息的输入顺序，依次输出每辆车的车牌号、最终保费和折扣。
**输入样例:**
```in
4
T001 T 20 1
C002 C 30 3
t003 t 40 5 100
c004 c 50 7 200
P c004 7 0
W T001 10 0
R t003 0
V C002 0
E
```
**输出样例:**
```out
T001 24000 1
C002 27825 1.05
t003 44650 0.95
c004 52150 1
```

**code:**

```c++
#include <iostream>
#include <string>
using namespace std;
class Vehicle
{
protected:
    string ID;
    int vehicle_price;
    int vehicle_age;
    double premium;
    double discount;
    bool is_renewal;
    bool has_violation;
public:
    Vehicle(string v_id, int v_p, int v_a=0){
        ID=v_id;
        vehicle_age=v_a;
        vehicle_price=v_p;
        discount=1.0;
        is_renewal=false;
        has_violation=false;
        premium=vehicle_price*(1.0-0.05*vehicle_age)*0.1*10000.0;
    }
    virtual double calc_premium();
    void calc_discount()
    {
        if (is_renewal) discount*=0.95;
        if (has_violation) discount*=1.05;
    }
    void set_renewal( ){is_renewal=true;}
    void set_violation( ){has_violation=true;}
    virtual void set(int w)=0;
    void display(){cout<<ID<<' '<<premium<<' '<<discount<<endl;}
    friend int find(Vehicle **, string,int);
};
double Vehicle::calc_premium()
{
    premium*=discount;
    return premium;
}
class EV: virtual public Vehicle
{
protected:
    int energe;
public:
    EV(string v_id, int v_p, int e,int v_a=0):Vehicle(v_id,v_p,v_a){
        energe=e;
        premium=premium*1.5;
    }
    virtual double calc_premium();
};
double EV::calc_premium()
{
    premium+=energe*10.0;
    premium=Vehicle::calc_premium();
    return premium;
    
}

class truck:virtual public Vehicle
{
protected:
    int weight;
public:
    truck(string v_id, int v_p,int v_a=0, int w=2) : Vehicle(v_id,v_p,v_a){
        weight=w;
    }
    virtual void set(int w){weight=w;}
    virtual double calc_premium();
};
double truck::calc_premium(){
    premium+=weight*500.0;
    premium=Vehicle::calc_premium();
    return premium;
}

class car: virtual public Vehicle
{
protected:
    int passage_num;
public:
    car(string v_id, int v_p,int v_a=0, int p=5):Vehicle(v_id,v_p,v_a){
        passage_num=p;
    }
    virtual void set(int p){passage_num=p;}
    virtual double calc_premium();
};

double car::calc_premium(){
    premium += passage_num*200.0;
    premium = Vehicle::calc_premium();
    return premium;
}
class e_truck: public truck, public EV
{
public:
    e_truck(string v_id, int v_p, int e, int v_a=0, int w=2) : Vehicle(v_id,v_p,v_a), truck(v_id,v_p,v_a,w), EV(v_id,v_p,e,v_a){}
    virtual double calc_premium();
};
double e_truck::calc_premium()
{
    premium+=weight*500.0+energe*10.0;
    premium=Vehicle::calc_premium();
    return premium;
}
class e_car: public car, public EV
{
public:
    e_car(string v_id, int v_p, int e,int v_a=0,int p=5) : Vehicle(v_id,v_p,v_a), car(v_id,v_p,v_a,p), EV(v_id,v_p,e,v_a){}
    virtual double calc_premium();
};
double e_car::calc_premium(){
    premium+=energe*10.0+passage_num*200.0;
    premium=Vehicle::calc_premium();
    return premium;
}
int find(Vehicle** p, string id, int num){
    int index=0;
    for (;index < num;index++)if (p[index]->ID==id) break;
    return index;
}

int main(){
    int num;
    Vehicle** p;
    cin>>num;
    if (num>0){
        p=new Vehicle * [num];
        for (int i=0;i<num;i++){
            string v_ID;
            cin>>v_ID;
            char type;
            cin>>type;
            int v_p, v_a,v_e;
            cin>>v_p>>v_a;
            switch (type){
                case 'T':p[i]=new truck(v_ID,v_p,v_a); break;
                case 'C':p[i]=new car(v_ID,v_p,v_a); break;
                case 't':cin>>v_e;p[i]=new e_truck(v_ID,v_p,v_e,v_a); break;
                case 'c':cin>>v_e;p[i]=new e_car(v_ID,v_p,v_e,v_a); break;
            }
        }
        char type;
        cin>>type;
        while (type!='E'){
            string v_ID;
            switch (type){
                case 'P':int v_p;cin>>v_ID; while (v_ID!="0"){cin>>v_p;int index=find(p,v_ID,num);p[index]->set(v_p);cin>>v_ID;};break;
                case 'R':cin>>v_ID;while (v_ID!="0"){int index=find(p,v_ID,num);p[index]->set_renewal( );cin>>v_ID;};break;
                case 'V':cin>>v_ID;while (v_ID!="0"){int index=find(p,v_ID,num);p[index]->set_violation( );cin>>v_ID;};break;
                case 'W':int w;cin>>v_ID; while (v_ID!="0"){cin>>w;int index=find(p,v_ID,num);p[index]->set(w);cin>>v_ID;};break;
            }
            cin>>type;
        }
        for (int i=0;i<num;i++){
            p[i]->calc_discount();
            p[i]->calc_premium();
        }
        for (int i=0; i<num; i++)p[i]->display();
    }
    return 0;
}
```


------

#### 主观题

##### 1.OOP VS. OPP

作为未来的软件开发工程师，编程时通常强调提高代码的可读性、可重用性、程序健壮性、可移植性、可维护性。请结合实践，选择其中一个方面谈谈你对面向对象程序设计在这方面表现的理解。


------
