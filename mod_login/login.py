from flask import Blueprint, render_template, request, redirect, url_for, session
from funcoes import Funcoes
from functools import wraps


bp_login = Blueprint('login', __name__, url_prefix='/', template_folder='templates')
@bp_login.route("/", methods=['GET', 'POST'])
def login():
	return render_template("formLogin.html")
@bp_login.route('/login', methods=['POST'])
def validaLogin():
    try:
        # dados enviados via FORM
        cpf = request.form['usuario']
        senha = Funcoes.cifraSenha(request.form['senha'])
        nomes = ["Pedro","João" ]
        grupo = ["Atendente (0)", "Caixa (1)","Administrador (2)"]

        # limpa a sessão
        session.clear()
        # Na minha aplicação somente dois funcionários diferentes que se cadastraram podem se logar 
        if (cpf == "536.528.923-65" and senha == Funcoes.cifraSenha('12345678')  ):
            # registra usuário na sessão, armazenando o login do usuário
            session['login'] = nomes[0] 
            session['cpf'] = cpf
            session['grupo'] = grupo[1]
            

            # abre a aplicação na tela home
            return redirect(url_for('index.formIndex'))
        elif( cpf == "123.123.321-32" and senha == Funcoes.cifraSenha('12345678') ):
            session['login'] = nomes[1]
            session['cpf'] = cpf
            session['grupo'] = grupo[2]

            return redirect(url_for('index.formIndex'))
        else:
            raise Exception("Falha de Login! As credenciais estão erradas")

    except Exception as e:
        # retorna para a tela de login
        return redirect(url_for('login.login', msgErro=e.args[0]))  

@bp_login.route("/logoff", methods=['GET'])
def logoff():
    # limpa um valor individual
    session.pop('login', None)
    # limpa toda sessão
    session.clear()
    # retorna para a tela de login
    return redirect(url_for('login.login'))

# valida se o usuário esta ativo na sessão
def validaSessao(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'login' not in session:
            # descarta os dados copiados da função original e retorna a tela de login
            return redirect(url_for('login.login', msgErro='Usuário não logado - Acesso Negado'))
        else:
            # retorna os dados copiados da função original
            return f(*args, **kwargs)
    # retorna o resultado do if acima
    return decorated_function
