# Importação de Bibliotecas
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
import matplotlib.pyplot as plt
# Classe do menu principal
class auth:
    def __init__(self,base):
# Criação do menu principal no Tkinter
        self.base=base
        self.base.title("Menu de Autenticação")
# Importação dos arquivos CSV para DataFrames ao iniciar
        self.usr_df=self.imp_usr_csv()
        self.lvr_df=self.imp_lvr_csv()
        self.emp_df=self.imp_emp_csv()
# Limpando o status de login
        self.usr_lgd=None
# Adicionando campos da interface
        self.lbl_usr=tk.Label(base,text="Usuário:")
        self.lbl_usr.pack()
        self.entr_usr=tk.Entry(base)
        self.entr_usr.pack()
        self.lbl_pwd=tk.Label(base,text="Senha:")
        self.lbl_pwd.pack()
        self.entr_pwd=tk.Entry(base,show="*")
        self.entr_pwd.pack()
        self.lgn_btn=tk.Button(base,text="Autenticar",command=self.lgn)
        self.lgn_btn.pack()
        self.rgs_btn=tk.Button(base, text="Registrar", command=self.rgs)
        self.rgs_btn.pack()
# Função para importar os dados de usuários de "usuarios.csv"
    def imp_usr_csv(self):
        try:
            usr_df=pd.read_csv("usuarios.csv")
        except FileNotFoundError:
            usr_df=pd.DataFrame(columns=["Nome", "ID", "Senha", "Tipo"])
        return usr_df
# Função para guardar novamente os dados de usuários em "usuarios.csv"    
    def exp_usr_csv(self):
        self.usr_df.to_csv("usuarios.csv",index=False)
# Função para importar o catálogo de livros em "livros.csv"
    def imp_lvr_csv(self):
        try:
            lvr_df=pd.read_csv("livros.csv")
        except FileNotFoundError:
            lvr_df=pd.DataFrame(columns=["ID", "Nome", "Quantidade"])
        return lvr_df
# Função para guardar novamente o catálogo de livros em "livros.csv"  
    def exp_lvr_csv(self):
        self.lvr_df.to_csv("livros.csv",index=False)
# Função para importar os livros emprestados em "emprestados.csv"
    def imp_emp_csv(self):
        try:
            emp_df=pd.read_csv("emprestados.csv")
        except FileNotFoundError:
            emp_df=pd.DataFrame(columns=["ID do Livro", "ID do Usuário"])
        return emp_df
# Função para guardar novamente os livros emprestados em "emprestados.csv"
    def exp_emp_csv(self):
        self.emp_df.to_csv("emprestados.csv",index=False)
# Menu de opções após a autenticação do usuário
    def esc_opcs(self):
        self.opcs=tk.Toplevel(self.base)
        ges_cat_mn_btn=tk.Button(self.opcs, text="Gestão do Catálogo",command=self.opc_ges_cat)
        ges_cat_mn_btn.pack()
        emp_mn_btn=tk.Button(self.opcs, text="Empréstimos e Devoluções",command=self.opc_emp)
        emp_mn_btn.pack()
        rlt_mn_btn=tk.Button(self.opcs, text="Relatórios",command=self.opc_rlt)
        rlt_mn_btn.pack()
        lgt_btn=tk.Button(self.opcs, text="Deslogar",command=self.lgt)
        lgt_btn.pack()
        # Condicional para que o usuário comum tenha acesso somente ao menu de empréstimos
        if self.usr_lgd["Tipo"].iloc[0]!="admin":
            ges_cat_mn_btn["state"]=tk.DISABLED
            rlt_mn_btn["state"]=tk.DISABLED
    # Menu de opções para a escolha de gestão de catálogo
    def opc_ges_cat(self):
        self.ges_cat_mn=tk.Toplevel(self.opcs)
        adc_btn=tk.Button(self.ges_cat_mn,text="Adicionar Livro",command=self.adc_lvr)
        adc_btn.pack()
        rm_btn=tk.Button(self.ges_cat_mn,text="Remover Livro",command=self.rm_lvr)
        rm_btn.pack()
        vlt_btn=tk.Button(self.ges_cat_mn,text="Voltar",command=self.ges_cat_mn.destroy)
        vlt_btn.pack()
    # Menu de opções para a escolha de empréstimo e devolução
    def opc_emp(self):
        self.emp_mn=tk.Toplevel(self.opcs)
        emp_btn=tk.Button(self.emp_mn,text="Empréstimo",command=self.emp_lvr)
        emp_btn.pack()
        dev_btn=tk.Button(self.emp_mn,text="Devolução",command=self.dev_lvr)
        dev_btn.pack()
        vlt_btn=tk.Button(self.emp_mn,text="Voltar",command=self.emp_mn.destroy)
        vlt_btn.pack()
    # Menu de opções para a escolha de relatórios
    def opc_rlt(self):
        self.rlt_mn=tk.Toplevel(self.opcs)
        mais_emp_btn=tk.Button(self.rlt_mn, text="Livros mais emprestados", command=self.mais_emp)
        mais_emp_btn.pack()
        frq_clnt_btn=tk.Button(self.rlt_mn, text="Clientes mais frequentes", command=self.frq_clnt)
        frq_clnt_btn.pack()
        rel_emp_btn=tk.Button(self.rlt_mn, text="Relação de emprestados e disponíveis", command=self.rel_emp)
        rel_emp_btn.pack()
        vlt_btn=tk.Button(self.rlt_mn, text="Voltar", command=self.rlt_mn.destroy)
        vlt_btn.pack()
    # Opção de deslogar
    def lgt(self):
        self.opcs.destroy()
        self.base.deiconify()
    # Função para autenticação dos dados de login
    def lgn(self):
        usr=self.entr_usr.get()
        pwd=self.entr_pwd.get()
        usr_inf=self.usr_df[(self.usr_df["Nome"]==usr)&(self.usr_df["Senha"]==pwd)]
        if not usr_inf.empty:
            self.usr_lgd=usr_inf
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo,{usr}!")
            self.esc_opcs()
            self.base.withdraw()
        else:
            messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")
    # Função para registro de novos dados de login
    def rgs(self):
        usr=self.entr_usr.get()
        pwd=self.entr_pwd.get()
        # Evitar conflitos de nome de usuário
        if not self.usr_df[self.usr_df["Nome"]==usr].empty:
            messagebox.showerror("Indisponível", "Usuário já registrado.")
        # Fornecendo ao usuário um ID, considerando uma ordem, evitando aqueles já utilizados
        else:
            nv_id=1 if self.usr_df.empty else self.usr_df["ID"].max()+1
            if "Senha" not in self.usr_df.columns:
                self.usr_df["Senha"]=""
            usr_tp="admin" if usr=="admin" else "cliente"
            usr_nv=pd.DataFrame({"Nome":[usr],"ID":[nv_id],"Senha":[pwd],"Tipo":[usr_tp]})
            self.usr_df=pd.concat([self.usr_df, usr_nv],ignore_index=True)
            self.exp_usr_csv()
            messagebox.showinfo("Registro bem-sucedido", "Usuário registrado com sucesso.")
    # Função para adicionar novos livros
    def adc_lvr(self):
        lvr_nm=simpledialog.askstring("Adicionar Livro","Nome do Livro:")
        if not lvr_nm:
            messagebox.showwarning("Aviso", "O nome do livro não pode estar vazio.")
            return
        lvr_qtd=simpledialog.askinteger("Adicionar Livro","Quantidade disponível:")
        if lvr_qtd is None:
            messagebox.showwarning("Aviso", "A quantidade do livro não pode estar vazia.")
            return
        lvr_id=1 if self.lvr_df.empty else self.lvr_df["ID"].max() + 1
        lvr_nv=pd.DataFrame({"ID":[lvr_id],"Nome":[lvr_nm],"Quantidade":[lvr_qtd]})
        self.lvr_df=pd.concat([self.lvr_df, lvr_nv],ignore_index=True)
        self.exp_lvr_csv()
        messagebox.showinfo("Adicionar Livro",f"Livro '{lvr_nm}' adicionado com sucesso!")
    # Função para remover livros do catálogo
    def rm_lvr(self):
        lvr_lst="\n".join([f"{livro['ID']} ({livro['Nome']})" for _, livro in self.lvr_df.iterrows()])
        to_rm_lvr=simpledialog.askinteger("Remover Livro", f"Escolha um livro para remover:\n{lvr_lst}")
        if to_rm_lvr in self.lvr_df["ID"].values:
            prmpt_cfrm=messagebox.askquestion("Remover Livro", "Deseja remover todas as unidades?")
            if prmpt_cfrm=="yes":
                self.lvr_df=self.lvr_df[self.lvr_df["ID"]!=to_rm_lvr]
                self.exp_lvr_csv()
                messagebox.showinfo("Remover Livro",f"Livro ID {to_rm_lvr} removido completamente.")
            else:
                rm_lvr_qtd=simpledialog.askinteger("Remover Livro","Quantidade a ser removida:")
                lvr_pos=self.lvr_df.index[self.lvr_df["ID"]==to_rm_lvr].tolist()[0]
                self.lvr_df.at[lvr_pos,"Quantidade"]-=rm_lvr_qtd
                self.exp_lvr_csv()
                messagebox.showinfo("Remover Livro", f"Quantidade de '{to_rm_lvr}' diminuída.")
        else:
            messagebox.showerror("Remover Livro", "Livro não encontrado.")
    # Função para fazer empréstimo de livro
    def emp_lvr(self):
        lvr_dsp_lst="\n".join([f"{livro['ID']} ({livro['Nome']})" for _, livro in self.lvr_df.iterrows()])
        id_lvr_esc=simpledialog.askinteger("Devolução de Livro", f"Seus livros emprestados:\n{lvr_dsp_lst}\nDigite o ID do livro que deseja devolver:")
        if id_lvr_esc in self.lvr_df['ID'].values:
            nv_emp=pd.DataFrame({"ID do Livro":[id_lvr_esc],"ID do Usuário":[self.usr_lgd["ID"].iloc[0]]})
            self.emp_df=pd.concat([self.emp_df,nv_emp],ignore_index=True)
            self.exp_emp_csv()
            messagebox.showinfo("Empréstimo realizado",f"Livro ID {id_lvr_esc} emprestado com sucesso!")
        else:
            messagebox.showerror("Erro no empréstimo","ID do livro inválido. Tente novamente.")
    # Função para devolver livro
    def dev_lvr(self):
        # Obtém os livros emprestados pelo usuário logado
        lst_lvr_emp = self.emp_df[self.emp_df["ID do Usuário"] == self.usr_lgd["ID"].iloc[0]]
        if lst_lvr_emp.empty:
            messagebox.showinfo("Devolução de Livro", "Você não possui livros emprestados.")
        else:
            lst_id_lvr="\n".join([f"{livro['ID do Livro']}" for _, livro in lst_lvr_emp.iterrows()])
            id_lvr_dev=simpledialog.askinteger("Devolução de Livro", f"Seus livros emprestados:\n{lst_id_lvr}\nDigite o ID do livro que deseja devolver:")
            if id_lvr_dev in lst_lvr_emp["ID do Livro"].values:
                self.emp_df=self.emp_df[(self.emp_df["ID do Usuário"] != self.usr_lgd["ID"].iloc[0])|(self.emp_df["ID do Livro"]!=id_lvr_dev)]
                self.exp_emp_csv()
                lvr_cmp=self.lvr_df[self.lvr_df["ID"]==id_lvr_dev]
                if not lvr_cmp.empty:
                    self.lvr_df.at[lvr_cmp.index[0],"Quantidade"]+=1
                    self.exp_lvr_csv()
                messagebox.showinfo("Devolução de Livro",f"Livro ID {id_lvr_dev} devolvido com sucesso!")
            else:
                messagebox.showerror("Devolução de Livro", "Livro não encontrado nos empréstimos.")
    # Função para exibir o relátorio dos livros mais emprestados
    def mais_emp(self):
        emp_cnt=self.emp_df['ID do Livro'].value_counts()
        if emp_cnt.empty:
            messagebox.showinfo("Relatório de Livros Mais Emprestados","Não há empréstimos registrados.")
        else:
            livros_nomes = self.lvr_df.set_index('ID').loc[emp_cnt.index,'Nome']
            plt.bar(livros_nomes, emp_cnt.values)
            plt.xlabel('ID do Livro')
            plt.ylabel('Quantidade de Empréstimos')
            plt.title('Livros Mais Emprestados')
            plt.xticks(rotation=45,ha='right')
            plt.show()
    # Função para exibir o relatório dos clientes mais frequentes
    def frq_clnt(self):
        emp_cnt=self.emp_df['ID do Usuário'].value_counts()
        if emp_cnt.empty:
            messagebox.showinfo("Relatório de Clientes Mais Frequentes","Não há empréstimos registrados.")
        else:
            clientes_nomes = self.usr_df.set_index('ID').loc[emp_cnt.index,'Nome']
            plt.bar(clientes_nomes, emp_cnt.values)
            plt.xlabel('ID do Cliente')
            plt.ylabel('Quantidade de Empréstimos')
            plt.title('Clientes Mais Frequentes')
            plt.xticks(rotation=45, ha='right')
            plt.show()
    # Função para exibir o relatório de relação entre emprestados e disponíveis
    def rel_emp(self):
        sm_lvr_dsp=self.lvr_df['Quantidade'].sum()
        sm_lvr_emp=self.emp_df.shape[0]
        lbl_rel=['Livros Disponíveis','Livros Emprestados']
        plt.pie([sm_lvr_dsp,sm_lvr_emp], labels=lbl_rel,autopct='%1.1f%%',startangle=90)
        plt.axis('equal')
        plt.title('Relação de Livros Emprestados e Disponíveis')
        plt.show()
# Iniciar a interface
if __name__ == "__main__":
    base=tk.Tk()
    app=auth(base)
    base.mainloop()