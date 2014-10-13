---
layout: default
---

---
layout: default
---

# Лекция 2

## <a name="1"></a> Функции

```cpp
int abs(int x) {
    return x > 0 ? x : -x;  // После этого сразу выход из функции
}

// Функция, возвращающая void — процедура
void print(int i) {
    cout << "Значение = " << i;
}
```

### <a name="2"></a> Стандартные функции

Математические функции объявлены в заголовочном файле
[&lt;cmath>](http://www.cplusplus.com/reference/cmath/).

```cpp
#include <cmath>
abs(x);  floor(x);  sin(x);  pow(x, y);  sqrt(x);
```

### <a name="3"></a> inline-функции

Для *маленьких* функций накладные расходы на вызов функции значительно 
превышают вычисления, производимые внутри функции. Поэтому такую функцию можно 
сделать *встраиваемой*: при компиляции тело будет встроено на место её вызова.

```cpp
inline int add(int a, int b) {
    return a + b;
}

int a = 3;
int c = add(a, 5);    // int c = a + 5;
```

Слово `inline` является лишь *рекомендацией* компилятору. На секунду вам 
может показаться, что вы умнее компилятора и сами знаете, какую функцию 
необходимо делать встраиваемой; в такой момент некоторые компиляторы могут даже 
[поддаться](http://stackoverflow.com/questions/25832402/can-we-force-the-function-to-be-inline-in-c) 
вам, но помните: вы не умнее.

## <a name="4"></a> Ссылки

Ссылка — другое имя объекта («псевдоним»). Ссылка всегда инициализируется
при объявлении.

```cpp
int i = 5;
int &pi = i;   // ссылка на i

pi = 3;
cout << i;     // i == 3
```

### <a name="5"></a> Передача аргумента в функцию по ссылке
```cpp
void calcSquareAndPerimeter(double a, double b, double &S, double &P) {
    S = a * b;
    P = 2 * (a + b);
}

int main() {
    double SS = 0.0, PP = 0.0;
    calcSquareAndPerimeter(3.0, 4.0, SS, PP);
    cout << "Perimeter: " << PP << ", Square: " << SS << "\n";
}
```

## <a name="6"></a> Структуры
```cpp
struct Student {
    string name;
    int age;
};  // точка с запятой!

int main() {
    Student s {"Иванов", 19};               // Инициализация
    cout << s.name << ' ' << s.age << endl;
    
    Student s2 = s;                         // Независимая копия s
    s2.name = "Петров";
    cout << s.name;                         // "Иванов"
}
```

### <a name="7"></a> Передача структуры в функцию

Желательно передавать структуру в функцию по ссылке, иначе будет передана её полная копия; `const` запрещает изменение полей структуры.

```cpp
void print(const Student &s) {
    cout << s.name << ' ' << s.age << endl;
}
```
