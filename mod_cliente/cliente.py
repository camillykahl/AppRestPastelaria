from flask import Blueprint, render_template, request, redirect, url_for
import requests
from funcoes import Funcoes
bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')
''' endereços do endpoint '''
urlApiClientes= "http://localhost:8000/cliente/"
urlApiCliente = "http://localhost:8000/cliente/%s"
headers = {'x-token': 'abcBolinhasToken', 'x-key': 'abcBolinhasKey'}
''' rotas dos formulários '''
@bp_cliente.route('/', methods=['GET', 'POST'])
def formListaCliente():
    try:
        response = requests.get(urlApiClientes, headers=headers)
        result = response.json()
        if(response.status_code != 200):
            raise Exception(result)
        return render_template('formListaCliente.html', result=result)
    except Exception as e:
        return render_template('formListaCliente.html', erro = e)


@bp_cliente.route('/form-cliente/', methods=['GET', 'POST'])
def formCliente():
    return render_template('formCliente.html')

@bp_cliente.route('/insert', methods=['POST'])
def insert():
    try:
    # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        compra_fiado = request.form['compra']
        dia_fiado = request.form['dia']
        senha = Funcoes.cifraSenha(request.form['senha'])
# monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone, 'compra_fiado': compra_fiado, 'dia_fiado': dia_fiado, 'senha': senha}
# executa o verbo POST da API e armazena seu retorno
        response = requests.post(urlApiClientes, headers=headers, json=payload)
        result = response.json()
        return redirect( url_for('cliente.formListaCliente', msg=result) )
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e)
