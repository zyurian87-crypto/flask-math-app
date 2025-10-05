import logging
import random
from flask import Flask, render_template, request

logger=logging.getLogger('LoggingTest')
sh=logging.StreamHandler()
logger.addHandler(sh)

logger.log(20,'info')
logger.log(30,'warnig')
logger.log(100,'test')

sh=logging.StreamHandler()

def generate_problem():
    """(x + a)³ の形式の問題を生成する関数"""
    a = random.choice([i for i in range(-10, 11) if i !=0])

    #問題の文字列を作成
    if a < 0:
        problem = f'(x - {-a})³'
    else:
        problem = f'(x + {a})³'

    #解答を計算(展開公式: (x + a)³ = x³ + 3ax² + 3a²x + a³)
    #  x³の係数
    coeff3 = 1
    #  x²の係数 
    coeff2 = 3 * a
    #  xの係数
    coeff1 = 3 * (a**2)
    #  定数項
    const = a**3

    answer = f'x³ + ({coeff2}x² + ({coeff1})x + ({const}))'
    
    answer = answer.replace('+ (-', '- ').replace(')', '').replace('(', '')

    return problem, answer

def generate_problem_patern2():
    # (ax + b)³ の形式
    a = random.randint(2, 5)
    b = random.choice([i for i in range(-10, 11)if i !=0])
    if b < 0: problem = f'({a}x - {-b})³'
    else: problem = f'({a}x + {b})³'
    coeff3 = a**3
    coeff2 = 3 * (a**2) * b
    coeff1 = 3* a* (b**2)
    const = b**3
    answer = f"{coeff3}x³ + ({coeff2})x² + ({coeff1})x + ({const})"
    answer = answer.replace('+ (-', '- ').replace(')', '').replace('(', '')
    return problem, answer

def generate_problem_patern3():
    # (ax + by)³
    a = random.randint(2, 5)
    b = random.choice([i for i in range(-10, 11)if i !=0])
    if b < 0: 
        
        problem = f'({a}x - {-b}y)³'
    else: 
        problem = f'({a}x + {b}y)³'
    # 回答を計算((ax+by)³ = (ax)³ + 3(ax)²(by) + 3(ax)(by)² + (by)³)
    coeff3 = a**3
    coeff2 = 3 * (a**2) * b  
    coeff1 = 3 * a * (b**2)
    const = b **3
    answer = f'{coeff3}x³ + {coeff2}x²y + {coeff1}xy² + {const}y³'
    answer = answer.replace('+ (-', '- ').replace(')', '').replace('(', '')
    return problem, answer

def generate_problem_patern4():
    #(x + a)(x² - ax + a²)のパターン
    a = random.randint(2, 10)
    problem = f'(x+{a}) (x² - {a}x + {a**2})'
    answer = f'x³ + {a**3}'
    return problem, answer

def generate_problem_patern5():
    #(x - a)(x² + ax + a²)のパターン
    a = random.randint(2, 10)
    problem = f'(x-{a})(x² + {a}x + {a**2})'
    answer = f'x³-{a**3}'
    return problem, answer

def generate_problem_patern6():
    """(x - a)³ の形式の問題を生成する関数"""
    a = random.randint(2, 10) # 正の整数aを使う
    problem = f'(x - {a})³'
    # 解答を計算: (x - a)³ = x³ - 3ax² + 3a²x - a³
    coeff2 = -3 * a
    coeff1 = 3 * (a**2)
    const = -(a**3)
    answer = f'x³ - {abs(coeff2)}x² + {coeff1}x - {abs(const)}'
    return problem, answer

def generate_problem_patern7():
    """(x+y+a)(x²+y²+a²-xy-ay-ax) の形式の問題を生成する関数"""
    a = random.randint(2, 9)
    problem = f'(x + y + {a})(x² + y² + {a*a} - xy - {a}y - {a}x)'
    answer = f'x³ + y³ + {a**3} - {3*a}xy'
    return problem, answer

problem_generators = [generate_problem, generate_problem_patern2, generate_problem_patern3, generate_problem_patern4, generate_problem_patern5, generate_problem_patern6, generate_problem_patern7]

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    title = '３乗の展開プリント'

    problems = None
    answers = None
    if request.method == 'POST':

        problems = []
        answers = []

        try:
            問題数 = int(request.form.get('num_problems', 10))

            for i in range(問題数):
                chosen_generator = random.choice(problem_generators)
                problem, answer = chosen_generator()
                problems.append(f'({i+1}) {problem} ')
                answers.append(f'({i+1}) {answer}')


        except ValueError:
            問題数 = 10
    

    return render_template('index.html', title=title, problems=problems, answers=answers)

if __name__ =='__main__':
    app.run(port=8000, debug=True)

