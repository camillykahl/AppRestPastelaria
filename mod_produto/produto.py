from flask import Blueprint, render_template, request, redirect, url_for
import requests
import base64
bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')
''' endereços do endpoint '''
urlApiProdutos= "http://localhost:8000/produto/"
urlApiProduto = "http://localhost:8000/produto/%s"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}

''' rotas dos formulários '''
@bp_produto.route('/', methods=['GET', 'POST'])
def formListaProduto():
    try:
        response = requests.get(urlApiProdutos, headers=headers)
        result = response.json()
        if(response.status_code != 200):
            raise Exception(result)
        return render_template('formListaProduto.html', result=result)
    except Exception as e:
        return render_template('formListaProduto.html', erro = e)
@bp_produto.route('/form-produto/', methods=['GET', 'POST'])
def formProduto():
    return render_template('formProduto.html')


@bp_produto.route('/insert', methods=['POST'])
def insert():
    try:
        # dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        #foto = request.form['foto']
        valor_unitario = request.form['valor']
        # converte a foto em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")

        # monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'valor_unitario': valor_unitario, 'foto': foto}
        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(urlApiProdutos, headers=headers, json=payload)
        result = response.json()
        return redirect( url_for('produto.formListaProduto', msg=result) )
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e)