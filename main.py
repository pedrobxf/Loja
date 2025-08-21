import streamlit as st
import cliente as cl
import produto as pr
import venda as vd
from datetime import datetime

st.title("Gerenciamento de loja")

st.sidebar.title("Menu")

option_menu = st.sidebar.selectbox("Selecione uma seção", ["Clientes", "Produtos", "Vendas"])
if option_menu == "Clientes":
    option_clientes = st.selectbox("Selecione uma opção", ["Cadastrar Cliente", "Listar Clientes", "Atualizar Cliente", "Desativar Cliente"])
    if option_clientes == "Cadastrar Cliente":
        st.header("Cadastrar Novo Cliente")
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        data_nascimento = st.date_input("Data de Nascimento", min_value=datetime(1900, 1, 1).date(), max_value=datetime.now().date())
        fl_ativo = st.checkbox("Ativo", value=True)

        if st.button("Salvar"):
            novo_cliente = cl.Cliente(
                id=None,
                nome=nome,
                email=email,
                data_nascimento=data_nascimento,
                fl_ativo=fl_ativo
            )
            cl.criar_cliente(novo_cliente)
            st.success("Cliente adicionado com sucesso!")

    elif option_clientes == "Listar Clientes":
        st.header("Lista de Clientes")
        clientes = cl.buscar_clientes()
        if clientes:
            st.table([
                {
                    "ID": cliente.id,
                    "Nome": cliente.nome,
                    "Email": cliente.email,
                    "Data de Nascimento": cliente.data_nascimento.isoformat(),
                    "Ativo": "Sim" if cliente.fl_ativo else "Não"
                } for cliente in clientes
            ])
        else:
            st.write("Nenhum cliente cadastrado.")
    
    elif option_clientes == "Atualizar Cliente":
        st.header("Atualizar Cliente")
        clientes = cl.buscar_clientes()
        cliente_dict = {f"{cliente.id} - {cliente.nome}": cliente for cliente in clientes}
        selected_cliente_str = st.selectbox("Selecione um cliente para atualizar", list(cliente_dict.keys()))
        if selected_cliente_str:
            selected_cliente = cliente_dict[selected_cliente_str]
            nome = st.text_input("Nome", value=selected_cliente.nome)
            email = st.text_input("Email", value=selected_cliente.email)
            data_nascimento = st.date_input("Data de Nascimento", value=selected_cliente.data_nascimento)
            fl_ativo = st.checkbox("Ativo", value=selected_cliente.fl_ativo)

            if st.button("Atualizar"):
                selected_cliente.nome = nome
                selected_cliente.email = email
                selected_cliente.data_nascimento = data_nascimento
                selected_cliente.fl_ativo = fl_ativo
                cl.atualizar_cliente(selected_cliente)
                st.success("Cliente atualizado com sucesso!")

    elif option_clientes == "Desativar Cliente":
        st.header("Desativar Cliente")
        clientes = cl.buscar_clientes()
        cliente_dict = {f"{cliente.id} - {cliente.nome}": cliente for cliente in clientes}
        selected_cliente_str = st.selectbox("Selecione um cliente para desativar", list(cliente_dict.keys()))
        if selected_cliente_str:
            selected_cliente = cliente_dict[selected_cliente_str]
            if st.button("Desativar Cliente"):
                cl.desativar_cliente(selected_cliente.id)
                st.success("Cliente desativado com sucesso!")

elif option_menu == "Produtos":
    option_produtos = st.selectbox("Selecione uma opção", ["Cadastrar Produto", "Listar Produtos", "Atualizar Produto"])
    if option_produtos == "Cadastrar Produto":
        st.header("Cadastrar Novo Produto")
        nome = st.text_input("Nome do Produto")
        descricao = st.text_area("Descrição do Produto")
        preco = st.number_input("Preço", min_value=0.0, format="%.2f")
        quantidade_estoque = st.number_input("Quantidade em Estoque", min_value=0)

        if st.button("Salvar"):
            novo_produto = pr.Produto(
                id=None,
                nome=nome,
                descricao=descricao,
                preco=preco,
                quantidade_estoque=quantidade_estoque
            )
            pr.criar_produto(novo_produto)
            st.success("Produto adicionado com sucesso!")
    
    elif option_produtos == "Listar Produtos":
        st.header("Lista de Produtos")
        produtos = pr.buscar_produtos()
        if produtos:
            st.table([
                {
                    "ID": produto.id,
                    "Nome": produto.nome,
                    "Descrição": produto.descricao,
                    "Preço": f"R$ {produto.preco:.2f}",
                    "Quantidade em Estoque": produto.quantidade_estoque
                } for produto in produtos
            ])
        else:
            st.write("Nenhum produto cadastrado.")
    
    elif option_produtos == "Atualizar Produto":
        st.header("Atualizar Produto")
        produtos = pr.buscar_produtos()
        produto_dict = {f"{produto.id} - {produto.nome}": produto for produto in produtos}
        selected_produto_str = st.selectbox("Selecione um produto para atualizar", list(produto_dict.keys()))
        if selected_produto_str:
            selected_produto = produto_dict[selected_produto_str]
            nome = st.text_input("Nome do Produto", value=selected_produto.nome)
            descricao = st.text_area("Descrição do Produto", value=selected_produto.descricao)
            preco = st.number_input("Preço", min_value=0.0, format="%.2f", value=float(selected_produto.preco))
            quantidade_estoque = st.number_input("Quantidade em Estoque", min_value=0, value=selected_produto.quantidade_estoque)

            if st.button("Atualizar"):
                selected_produto.nome = nome
                selected_produto.descricao = descricao
                selected_produto.preco = preco
                selected_produto.quantidade_estoque = quantidade_estoque
                pr.atualizar_produto(selected_produto)
                st.success("Produto atualizado com sucesso!")

elif option_menu == "Vendas":
    option_vendas = st.selectbox("Selecione uma opção", ["Registrar Venda", "Listar Vendas", "Excluir Venda"])
    if option_vendas == "Registrar Venda":
        st.header("Registrar Nova Venda")
        clientes = cl.buscar_clientes()
        produtos = pr.buscar_produtos()

        cliente_dict = {f"{cliente.id} - {cliente.nome}": cliente for cliente in clientes if cliente.fl_ativo}
        produto_dict = {f"{produto.id} - {produto.nome}": produto for produto in produtos if produto.quantidade_estoque > 0}

        selected_cliente_str = st.selectbox("Selecione um Cliente", list(cliente_dict.keys()))
        selected_produto_str = st.selectbox("Selecione um Produto", list(produto_dict.keys()))

        quantidade = st.number_input("Quantidade", min_value=1, value=1)
        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if st.button("Registrar Venda"):
            venda = vd.Venda(
                cliente_id=cliente_dict[selected_cliente_str].id,
                produto_id=produto_dict[selected_produto_str].id,
                quantidade=quantidade,
                data_venda=data_venda,
                preco_referencia=produto_dict[selected_produto_str].preco,
                total=produto_dict[selected_produto_str].preco * quantidade
            )
            if produto_dict[selected_produto_str].quantidade_estoque < quantidade:
                st.error("Quantidade em estoque insuficiente.")
            else:
                vd.criar_venda(venda)
                st.success("Venda registrada com sucesso!")

    elif option_vendas == "Listar Vendas":
        st.header("Lista de Vendas")
        vendas = vd.buscar_vendas()
        if vendas:
            st.table([
                {
                    "ID": venda.id,
                    "Produto": pr.produto_por_id(venda.produto_id).nome,
                    "Quantidade": venda.quantidade,
                    "Data da Venda": venda.data_venda,
                    "Preço de Referência": f"R$ {venda.preco_referencia}",
                    "Total": f"R$ {venda.total}",
                    "Cliente": cl.cliente_por_id(venda.cliente_id).nome,
                } for venda in vendas
            ])
        else:
            st.write("Nenhuma venda registrada.")

    elif option_vendas == "Excluir Venda":
        st.header("Excluir Venda")
        vendas = vd.buscar_vendas()
        venda_dict = {f"{venda.id} - Cliente ID: {venda.cliente_id}, Produto ID: {venda.produto_id}": venda for venda in vendas}
        selected_venda_str = st.selectbox("Selecione uma venda para excluir", list(venda_dict.keys()))
        if selected_venda_str:
            selected_venda = venda_dict[selected_venda_str]
            if st.button("Excluir Venda"):
                vd.excluir_venda(selected_venda.id)
                st.success("Venda excluída com sucesso!")
            

    