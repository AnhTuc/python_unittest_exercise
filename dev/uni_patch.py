import unittest
import sys
from unittest.mock import patch, NonCallableMock, Mock, MagicMock
from io import StringIO

class SomeClass:
    a= 10
    def __init__(self):
        self.a =10
        self.b =40
    def method(self,x):
        return 32+x
    def class_method(self):
        return 100

@patch.object(SomeClass, 'class_method')
def test_patch_object(mock_method):
    SomeClass.class_method(3)
    mock_method.assert_called_with(3)

@patch('sys.non_exist_att',42,create=True)
def test_patch_create():
    assert sys.non_exist_att == 42

@patch('__main__.SomeClass')
def test_create_mock(normal_arg, mock_class):
    print(mock_class is SomeClass)

@patch('__main__.SomeClass')
def test_return_value(mock_class):
    instance = mock_class.return_value
    instance.method.return_value ='foo'

    assert SomeClass() is instance
    assert SomeClass().method() == 'foo'

def test_spec():
    Original = SomeClass
    patcher = patch('__main__.SomeClass', spec= True)
    Mock_class = patcher.start()
    instance = Mock_class()

    assert isinstance(instance, Original)

    patcher.stop()

thing = object()
def test_new_callable():
    with patch('__main__.thing', new_callable=NonCallableMock) as mock_thing:
        assert thing is mock_thing
        try:
            thing()
        except Exception as e:
            print(e)

@patch('sys.stdout',new_callable=StringIO)
def test_std_out(mock_stdout):
    def foo():
        print("Writing something")
    
    foo()
    assert mock_stdout.getvalue() == 'Writing something\n'

def test_patch_config():
    with patch('__main__.thing', first =1, second ='foo') as mock_thing1:
        assert mock_thing1.first ==1
        assert mock_thing1.second =='foo'
    
    configs ={
        'f.return_value': 'foo1',
        'tmp': 3
    }
    with patch('__main__.thing',**configs) as mock_thing2:
        assert mock_thing2.f() == 'foo1'
        assert mock_thing2.tmp == 3

@patch('uni_patch.thing', first =1)
@patch('uni_patch.thing',**{'gv.return_value':45, 'o':0})
def test_patch_config2(mock_thing1, mock_thing2):
    assert mock_thing1.gv() == 45
    assert mock_thing1.o ==0

    assert mock_thing2.first ==1

def test_patch_config3():
    patcher =patch('__main__.thing',tmp_value=1)
    mock_obj = patcher.start()
    assert mock_obj.tmp_value == 1
    patcher.stop()
    try:
        assert mock_obj.tmp_value ==1
    except Exception as e:
        print(e)

def tmp(i):
    return i+32
#if you want to patch a function or a method of a class and keep the rest
@patch('uni_patch.tmp')
def test_patch_func(mock_f):
    mock_f.return_value =46
    assert mock_f() == 46
    assert mock_f(5) == 46

    with patch('__main__.SomeClass.class_method',Mock(return_value=3)):
        t = SomeClass()
        assert t.class_method(3) == 3
        assert t.method(3) == 35
    
    with patch('__main__.SomeClass.class_method'):
        SomeClass.class_method.return_value = 48
        t = SomeClass()
        assert t.class_method() ==48
        assert t.method(45) == 77

    with patch('__main__.SomeClass.class_method', return_value = 99, autospec=True):
        t = SomeClass()
        print("Patch one method can retrive a %d" %t.a)
        assert t.class_method() == 99
        try:
            print(t.class_method(45))
        except Exception as e:
            print(e)
        assert t.method(34) == 66
    
    m = MagicMock()
    m.method.return_value =9999
    m.class_method.return_value = 666

    with patch('__main__.SomeClass', return_value = m) as p:
        t = SomeClass()
        print(t.class_method())
        print(t.a)
        print(t.method())

def test_patch_dict():
    lib = {}
    with patch.dict(lib,{'new_key':'new_value'}) as patched_dict:
        print(lib['new_key'])
    



    


if __name__ =="__main__":
    test_patch_create()
    test_create_mock(None)
    test_return_value()
    test_new_callable()
    test_std_out()
    test_patch_config()
    test_patch_config2()
    test_patch_config3()
    test_patch_object()
    test_patch_func()
    test_patch_dict()