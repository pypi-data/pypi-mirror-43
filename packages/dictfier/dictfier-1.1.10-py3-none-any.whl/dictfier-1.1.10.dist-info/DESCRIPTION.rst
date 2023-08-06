Copyright (c) 2019 Yezy Ilomo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: dictfier
        ========
        
        |Build Status| |image| |image| |image|
        
        **dictfier** is a library to convert/serialize Python class
        instances(Objects) both **flat** and **nested** into a dictionary data
        structure. It's very useful in converting Python Objects into JSON
        format especially for nested objects, because they can't be handled well
        by json library
        
        Prerequisites
        ~~~~~~~~~~~~~
        
        python version >= 2.7
        
        Installing
        ~~~~~~~~~~
        
        For python3
        
        .. code:: python
        
            pip3 install dictfier
        
        For python2
        
        .. code:: python
        
            pip install dictfier
        
        Getting Started
        ---------------
        
        **Converting a flat object into a dict**
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
            student = Student("Danish", 24)
        
            query = [
                "name",
                "age"
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        **Converting nested object into a dict**
        
        .. code:: python
        
            import dictfier
        
            class Course(object):
                def __init__(self, code, name):
                    self.code = code
                    self.name = name
                    
            class Student(object):
                def __init__(self, name, age, course):
                    self.name = name
                    self.age = age
                    self.course = course
        
            course = Course("CS201", "Data Structures")
            student = Student("Danish", 24, course)
        
            query = [
                "name",
                "age",
                {
                    "course": [
                        "code",
                        "name",
                    ]
                }
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        **Converting object nested with iterable object into a dict**
        
        .. code:: python
        
            import dictfier
        
            class Course(object):
                def __init__(self, code, name):
                    self.code = code
                    self.name = name
                    
            class Student(object):
                def __init__(self, name, age, courses):
                    self.name = name
                    self.age = age
                    self.courses = courses
        
            course1 = Course("CS201", "Data Structures")
            course2 = Course("CS205", "Computer Networks")
        
            student = Student("Danish", 24, [course1, course2])
        
            query = [
                "name",
                "age",
                {
                    "courses": [
                        [
                            "code",
                            "name",
                        ]
                    ]
                }
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        **What about instance methods or callable object fields?**
        
        Well we've got good news for that, **dictfier** can use callables which
        return values as fields, It's very simple, you just have to pass
        "call\_callable=True" as a keyword argument to dictfy function and add
        your callable field to a query. E.g.
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
                def age_in_days(self):
                    return self.age * 365
        
            student = Student("Danish", 24)
        
            query = [
                "name",
                "age_in_days"
            ]
        
            std_info = dictfier.dictfy(student, query, call_callable=True)
            print(std_info)
        
        **You can also add your custom field by using "not\_found\_create=True"
        as a keyword argument. E.g.**
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
            student = Student("Danish", 24)
        
            query = [
                "name",
                "age",
                {
                    "school": "St Patrick"
                }
            ]
        
            std_info = dictfier.dictfy(student, query, not_found_create=True)
            print(std_info)
        
        **What if we want to use object field on a custom field to do some
        computations?.**
        
        Well there is a way to do that too, **dictfier** API provides **useobj**
        hook which is used to hook or pull the object on a current query node.
        To use the current object, just define a fuction which accept single
        argument(which is an object) and perform your computations on such
        function and then return a result, call **useobj** and pass that defined
        fuction to it.
        
        Let's say we want to calculate age of a student in terms of months from
        a student object with age field in terms of years. Here is how we would
        do this by using **useobj** hook.
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
            student = Student("Danish", 24)
        
            def age_in_months(obj):
                # Do the computation here then return the result
                return obj.age * 12
        
            query = [
                "name",
                
                # This is a custom field which is computed by using age field from a student object
                # Note how age_in_months function is passed to useobj hook(This is very important for API to work)
                {"age_in_months": dictfier.useobj(age_in_months)}
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        **What if we want to use object field on a custom field(Rename obj
        field)?**
        
        This can be accomplished in two ways, As you might have guessed, one way
        to do it is to use **useobj** hook by passing a function which return
        the value of a field which you want to use, another simple way is to use
        **usefield** hook. Just like **useobj** hook, **usefield** hook is used
        to hook or pull object field on a current query node. To use the current
        object field, just call **usefield** and pass a field name which you
        want to use or replace.
        
        Let's say we want to rename **age** field to **age\_in\_years** in our
        results. Here is how we would do this by using **usefield** hook.
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
            student = Student("Danish", 24)
        
            query = [
                "name",
                {"age_in_years": dictfier.usefield("age")}
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        And if you want to use **useobj** hook then this is how you would do it.
        
        .. code:: python
        
            import dictfier
        
            class Student(object):
                def __init__(self, name, age):
                    self.name = name
                    self.age = age
        
            student = Student("Danish", 24)
        
            query = [
                "name",
                {"age_in_years": dictfier.useobj(lambda obj: obj.name)}
            ]
        
            std_info = dictfier.dictfy(student, query)
            print(std_info)
        
        Infact **usefield** hook is implemented by using **useobj**, so both
        methods are the same interms of performance, but I think you would agree
        with me that in this case **usefield** is more readable than **useobj**.
        
        How dictfier works?
        -------------------
        
        **dictfier** works by converting given Object into a corresponding dict
        **recursively(Hence works on nested objects)** by using a **Query**. So
        what's important here is to know how to structure right queries to
        extract right data from the object.
        
        **What's a Query anyway?**
        
        A Query is basically a template which tells dictfier what to extract
        from an object. It is defined as a list or tuple of Object's fields to
        be extracted.
        
        **Sample conversions**.
        
        When a flat student object is queried using a query below
        
        .. code:: python
        
            query = [
                "name",
                "age",
            ]
        
        **dictfier** will convert it into
        
        .. code:: python
        
            {
                "name": student.name,
                "age": student.age,
            }   
        
        **For nested queries it goes like**
        
        .. code:: python
        
            query = [
                "name",
                "age",
                {
                    "course": [ 
                        "code",
                        "name",
                    ]
                }
            ]
        
        **Corresponding dict**
        
        .. code:: python
        
            {
                "name": student.name,
                "age": student.age,
                "course": {
                    "code": student.course.code,
                    "name": student.course.name,
                }
            }
        
        **For iterable objects it goes like**
        
        .. code:: python
        
            query = [
                "name",
                "age",
                {
                    "course": [ 
                        [
                            "code",
                            "name",
                        ]
                    ]
                }
            ]
        
        Putting a list or tuple inside a list or tuple of object fields is a way
        to declare that the Object is iterable. In this case
        
        .. code:: python
        
            [ 
                [
                    "code",
                    "name",
                ]
            ]
        
        **Corresponding dict**
        
        .. code:: python
        
            {
                "name": student.name,
                "age": student.age,
                "courses": [
                    {
                        "code": course.code,
                        "name": course.name,
                    }
                    for course in student.courses
                ]
            }
        
        Notice the list or tuple on "courses" unlike in other fields like "name"
        and "age", it makes "courses" iterable, This is the reason for having
        nested list or tuple on "courses" query.
        
        **It's pretty simple right?**
        
        .. |Build Status| image:: https://api.travis-ci.com/yezyilomo/dictfier.svg?branch=master
           :target: https://api.travis-ci.com/yezyilomo/dictfier
        .. |image| image:: https://img.shields.io/pypi/v/dictfier.svg
           :target: https://pypi.org/project/dictfier/
        .. |image| image:: https://img.shields.io/pypi/pyversions/dictfier.svg
           :target: https://pypi.org/project/dictfier/
        .. |image| image:: https://img.shields.io/pypi/l/dictfier.svg
           :target: https://pypi.org/project/dictfier/
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Developers
Classifier: Natural Language :: English
Classifier: License :: OSI Approved :: Apache Software License
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 2
Classifier: Programming Language :: Python :: 2.7
Classifier: Programming Language :: Python :: 3
Classifier: Programming Language :: Python :: 3.4
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3.6
Classifier: Programming Language :: Python :: 3.7
Classifier: Programming Language :: Python :: Implementation :: CPython
Classifier: Programming Language :: Python :: Implementation :: PyPy
Requires-Python: >=2.7
Description-Content-Type: text/x-rst
