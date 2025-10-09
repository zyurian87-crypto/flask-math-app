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
    """(x - a)³ の形式の問題"""
    a = random.randint(2, 10) # 正の整数aを使う
    problem = f'(x - {a})³'
    # 解答を計算: (x - a)³ = x³ - 3ax² + 3a²x - a³
    coeff2 = -3 * a
    coeff1 = 3 * (a**2)
    const = -(a**3)
    answer = f'x³ - {abs(coeff2)}x² + {coeff1}x - {abs(const)}'
    return problem, answer

def generate_problem_patern7():
    """(x+y+a)(x²+y²+a²-xy-ay-ax) の形式の問題"""
    a = random.randint(2, 9)
    problem = f'(x + y + {a})(x² + y² + {a*a} - xy - {a}y - {a}x)'
    answer = f'x³ + y³ - {3*a}xy + {a**3}'
    return problem, answer

def division_problem_patern1():
    a = random.randint(2, 10)
    problem = f'(x³ + {a**3}) ÷ (x+{a})'
    answer = f'(x² - {a}x + {a**2})'
    return problem, answer

def division_problem_patern2():
    a = random.randint(2, 10)
    problem = f'(x³ + {a**3}) ÷ (x² - {a}x + {a**2})'
    answer = f'(x+{a})'
    return problem, answer


cubed_expansion_generators = [generate_problem, generate_problem_patern2, generate_problem_patern3, generate_problem_patern4, generate_problem_patern5, generate_problem_patern6, generate_problem_patern7]

division_generators = [division_problem_patern1, division_problem_patern2]

all_generators = cubed_expansion_generators + division_generators

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    title = '３乗の展開プリント'

    problems = None
    answers = None
    num_problems = 10
    selected_genre = 'cubed'
    if request.method == 'POST':

        problems_list = []
        answers_list = []

        try:
            問題数 = int(request.form.get('num_problems', 10))
            selected_genre = request.form.get('genre', 'cubed')
    
            if selected_genre == 'cubed':
                target_generators = cubed_expansion_generators
                num_patterns = len(target_generators)
                if num_patterns == 0: raise IndexError('問題パターンがありません')

                base_count = 問題数 // num_patterns
                remainder = 問題数 % num_patterns

                temp_generators = []
                for i in range(num_patterns):
                    count = base_count
                    if i < remainder:
                        count += 1
                    temp_generators.extend([target_generators[i]] * count)
                random.shuffle(temp_generators)

                for generator_func in temp_generators:
                    problem, answer = generator_func()
                    problems_list.append(problem)
                    answers_list.append(answer)

            elif selected_genre == 'division':

                for i in range(問題数):
                    chosen_generator = random.choice(division_generators)
                    problem, answer = chosen_generator()
                    problems_list.append(problem)
                    answers_list.append(answer)

            else: # 'mixed'が選択された場合
                for i in range(問題数):
                    chosen_generator = random.choice(all_generators)
                    problem, answer = chosen_generator()
                    problems_list.append(problem)
                    answers_list.append(answer)
            
            problems = [f'({i+1}){p}' for i, p in enumerate(problems_list)]
            answers = [f'({i+1}){a}' for i, a in enumerate(answers_list)]

        except (ValueError, IndexError) as e:
            print(f'エラーが発生しました: {e}')
            問題数 = 10
            problems = None
            answers = None
    

    return render_template('index.html', 
                           title=title, 
                           problems=problems, 
                           answers=answers,
                           selected_genre=selected_genre)

if __name__ =='__main__':
    app.run(port=8000, debug=True)

