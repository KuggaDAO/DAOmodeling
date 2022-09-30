from behave import *
from Work import *
from Network import *
from Vote import *
from painter import *
from ruamel import yaml

#对.feature的处理用正则表达式
use_step_matcher("re")

@Given('I create (?P<number>\d+) works with (?P<test_configs>.*)')
def step_impl(context, number, test_configs):
    with open(test_configs, 'r') as f:
        context.configs = yaml.load(f, yaml.Loader)
    context.works = []
    for i in range(int(number)):
        context.works.append(Work(i, context.configs))

@Then('I see (?P<number>\d+) elements in (?P<text>.*)')
def step_impl(context, number, text):
    exec('assert(len(context.' + text +') == ' + number + ')')
