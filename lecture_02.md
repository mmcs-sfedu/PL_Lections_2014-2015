# Лекция 2

## Ссылки

Ссылка - другое имя объекта.

Ссылка инициализируется при объявлении.

### Передача аргумента в функцию по ссылке

	void CalcSP(double a, double b, double &S, double &D){
	
	  S = a*b;
	  P = 2*(a+b);
	}

	...
	
	double SS = 0.0, PP = 0.0;

	CalcSP(3.0, 4.0, SS, PP);


## Структуры

	struct Student{

	  string name;
	  int age;
	};
 
	Student s {"Иванов", 19}; // Инициализация

	cout << s.name << ' ' << s.age << endl;

### Передача структуры в функцию

Передача структуры в функцию происходит по ссылке

	void print(const Student &s){
	  cout << s.name << ' ' << s.age << endl;
	}
	
	...
	
	print(s);