import json
import pytest
from envision import envision
from os.path import isfile, join, exists
from os import remove, environ

def purge(p):
    if exists(p):
       remove(p)

def test_valid_dev():
    root = 'envision/tests/valid_dev'
    env = envision(root)    
    assert env.get('key') == 'value'
    env._envision__lock()
    assert isfile(join(root,'.envision.lock'))
    assert isfile(join(root,'.envision.key'))
    env2 = envision(root)
    assert env.key == env2.key
    purge(join(root,'.envision.lock'))
    purge(join(root,'.envision.key'))

def test_non_existent_root():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/non_existent'
        envision(root)
        
def test_empty_root():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/empty'
        envision(root)

def test_invalid_envision_file():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/invalid_envision_file'
        envision(root)

def test_invalid_envision_key_value():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/invalid_envision_key_value'
        envision(root)

def test_valid_prod():
    root = 'envision/tests/valid_prod'
    environ["ENVISION"] = "L7KWG5RD7MGWUPCD"
    env = envision(root)
    assert env.get('key') == 'value'

def test_non_existent_env_key():
    with pytest.raises(EnvironmentError):
        environ["ENVISION"] = "J2fHRC_5H629-8f1JSNDdw2FV0Hx2Eesly8JMe_MI3g="
        del environ["ENVISION"]
        root = 'envision/tests/valid_prod'
        envision(root)

def test_incorrect_env_key():
    with pytest.raises(EnvironmentError):
        environ["ENVISION"] = "J2fHRC_5H629-8f10SNDdw2FV0Hx2Eesly8JMe_MI3g="
        root = 'envision/tests/valid_prod'
        envision(root)

def test_invalid_envision_lock_file():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/invalid_envision_lock_file'
        envision(root)

def test_invalid_envision_lock_key_value():
    with pytest.raises(EnvironmentError):
        root = 'envision/tests/invalid_envision_lock_key_value'
        envision(root)

def test_git_warnings():
        with pytest.warns(Warning):
                root = 'envision/tests/git_warnings'
                envision(root)
                purge(join(root,'.envision.lock'))
                purge(join(root,'.envision.key'))

def test_dev_warnings():
        with pytest.warns(Warning):
                environ['ENVISION'] = "abc"
                root = 'envision/tests/dev_warnings'
                envision(root)
                purge(join(root,'.envision.lock'))
                purge(join(root,'.envision.key'))                

def test_prod_warnings():
        with pytest.warns(Warning):
                environ['ENVISION'] = "L7KWG5RD7MGWUPCD"
                root = 'envision/tests/prod_warnings'
                envision(root)

