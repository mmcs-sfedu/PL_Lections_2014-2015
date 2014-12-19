# Лекция 21

## all_of

```cpp
all_of(b, e, pred)
```

Возвращает true если все элементы удовлетворяют заданному предикату.

## equal

```cpp
equal(b, e, b1) 
{
	while(b != e)
	{
		if (*b1 != *b1)
			return false;
	++b;
	++b1;
	}
	return true;
}
```

## mismatch

если данны две последовательности:
1 5 7 3
1 5 4 8

Возвращается пара итераторов на несовпадающие элементы

```cpp
pair<InIt, InIt> mistmatch(b, e, b1)
{
	auto p = mistmatch(begin(v), end(v), begin(v1));
	if (p.first == end(v))
		cout << "equals";
	else cout << *(p.first) << *(p.second);
}
```

## search

Ищет подпоследовательность в последовательности

search(b, e, b1, e1)


## copy

```cpp
OutIt copy(InIt b, InIt e, OutIt b1)
{
	while(b != e) {
		*b1 != *b;
		++b;
		++b1;
	}
	return b1;
}
```

```cpp
vector<int> v{1, 5, 3};
list<int> l;
copy(begin(v), end(v), begin(l));
// Итератор будет иметь нулевое значение поэтому при попытке обратиться к нему произойдет ошибка.
```

## Итераторы вставки

Таким образом элементы копируются добавляясь в список:

```cpp
copy(begin(v), end(v), back_inserter(l));
```

```cpp
copy(begin(v), end(v), back_inserter_iterator<list<int>>)
```



```cpp
template<typename C>
class back_inserter_iterator
{
	C & c;
public:
	back_inserter_iterator(const C & cc): c(cc) {}
	back_inserter_iterator<C>& operator*()
	{
		return *this;
	}
	void operator =(const C::value_type& v)
	{
		c.push_back(v);
	}
	void operator++() {}
};
```

Теперь из back_inserter_iterator сделает back_inserter:

```cpp
inline
template<typename C>
back_insert)iterator<C> back_incerter(const C& c)
{
	return back_incert_iterator<C> (c);
}
```

Так же существует front_inserter, который копирует элементы в начало контейнера, который имеет функцию push_front.


## Итерторы потоков

Допустим нам надо копировать последовательность в поток. 

```cpp
vector<int> v{1, 5, 3};
// хочется написать так copy(begin(v), end(v), cout)
// На деле создается обертка над cout
copy(begin(v), end(v), ostream_iterator<int>(cout, " "));
```

```cpp
template<typename T>
class ostream_iterator
{
	ostream & os;
	string delim;
public:
	ostream_iterator(cout ostream& oos, const string& d): os(oss), delim(d){}
	void operator++(){}
	void operator=(const T & t)
	{
		os << t << delime;
	}
};
```


## Итератор потока ввода

```cpp
vector<int> v;
copy(istream_iterator<int>(cin), istream_iterator<int>(), back_incerter(v));
```

Если здесь файловый поток, то копироваться будут элементы до конца файла, если cin, то концом потока ввода будет символ генерируемый Ctrl+Z



В результате операий изменения контейнера все итераторы этого контейнера станут недействительными.







