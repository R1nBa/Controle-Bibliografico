import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pandas as pd
import matplotlib.pyplot as plt
class auth:
    def __init__(self,base):
        self.base=base
        self.base.title("Menu de Autenticação")
        self.usr_df=self.imp_usr_csv()
        self.lvr_df=self.imp_lvr_csv()
        self.emp_df=self.imp_emp_csv()
        self.usr_lgd=None
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
    def imp_usr_csv(self):
        try:
            usr_df=pd.read_csv("usuarios.csv")
        except FileNotFoundError:
            usr_df=pd.DataFrame(columns=["Nome", "ID", "Tipo"])
        return usr_df
    def exp_usr_csv(self):
        self.usr_df.to_csv("usuarios.csv",index=False)
    def imp_lvr_csv(self):
        try:
            lvr_df=pd.read_csv("livros.csv")
        except FileNotFoundError:
            lvr_df=pd.DataFrame(columns=["ID", "Nome", "Quantidade"])
        return lvr_df
    def exp_lvr_csv(self):
        self.lvr_df.to_csv("livros.csv",index=False)
    def imp_emp_csv(self):
        try:
            emp_df=pd.read_csv("emprestados.csv")
        except FileNotFoundError:
            emp_df=pd.DataFrame(columns=["ID do Livro", "ID do Usuário"])
        return emp_df
    def exp_emp_csv(self):
        self.emp_df.to_csv("emprestados.csv",index=False)
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
        if self.usr_lgd["Tipo"].iloc[0]!="admin":
            ges_cat_mn_btn["state"]=tk.DISABLED
            rlt_mn_btn["state"]=tk.DISABLED
    def opc_ges_cat(self):
        self.ges_cat_mn=tk.Toplevel(self.opcs)
        adc_btn=tk.Button(self.ges_cat_mn,text="Adicionar Livro",command=self.adc_lvr)
        adc_btn.pack()
        rm_btn=tk.Button(self.ges_cat_mn,text="Remover Livro",command=self.rm_lvr)
        rm_btn.pack()
        vlt_btn=tk.Button(self.ges_cat_mn,text="Voltar",command=self.ges_cat_mn.destroy)
        vlt_btn.pack()
    def opc_emp(self):
        self.emp_mn=tk.Toplevel(self.opcs)
        emp_btn=tk.Button(self.emp_mn,text="Empréstimo",command=self.emp_lvr)
        emp_btn.pack()
        dev_btn=tk.Button(self.emp_mn,text="Devolução",command=self.dev_lvr)
        dev_btn.pack()
        vlt_btn=tk.Button(self.emp_mn,text="Voltar",command=self.emp_mn.destroy)
        vlt_btn.pack()
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
    def lgt(self):
        self.opcs.destroy()
        self.base.deiconify()
    def lgn(self):
        usr=self.entr_usr.get()
        pwd=self.entr_pwd.get()
        usr_inf=self.usr_df[(self.usr_df["Nome"]==usr)&(self.usr_df["ID"]==pwd)]
        if not usr_inf.empty:
            self.usr_lgd=usr_inf
            messagebox.showinfo("Login bem-sucedido", f"Bem-vindo,{usr}!")
            self.esc_opcs()
            self.base.withdraw()
        else:
            messagebox.showerror("Login inválido", "Usuário ou senha incorretos.")
    def rgs(self):
        usr=self.entr_usr.get()
        pwd=self.entr_pwd.get()
        if not self.usr_df[(self.usr_df["Nome"]==usr) & (self.usr_df["ID"]==pwd)].empty:
            messagebox.showerror("Indisponível", "Usuário já registrado.")
        else:
            usr_tp="admin" if usr == "admin" else "cliente"
            usr_nv=pd.DataFrame({"Nome": [usr],"ID": [pwd],"Tipo": [usr_tp]})
            self.usr_df=pd.concat([self.usr_df,usr_nv],ignore_index=True)
            self.exp_usr_csv()
            messagebox.showinfo("Registro bem-sucedido","Usuário registrado com sucesso.")
    def adc_lvr(self):
        lvr_nm=simpledialog.askstring("Adicionar Livro", "Nome do Livro:")
        lvr_id=simpledialog.askstring("Adicionar Livro", "ID do Livro:")
        lvr_qtd=simpledialog.askinteger("Adicionar Livro", "Quantidade disponível:")
        lvr_nv=pd.DataFrame({"ID": [lvr_id], "Nome": [lvr_nm], "Quantidade": [lvr_qtd]})
        self.lvr_df=pd.concat([self.lvr_df, lvr_nv],ignore_index=True)
        messagebox.showinfo("Adicionar Livro", f"Livro '{lvr_nm}' adicionado com sucesso!")
    def rm_lvr(self):
        lvr_lst="\n".join(self.lvr_df["Nome"])
        rm_lvr=simpledialog.askstring("Remover Livro", f"Escolha um livro para remover:\n{lvr_lst}")
        if to_rm_lvr in self.lvr_df["Nome"].values:
            prmpt_cfrm=messagebox.askquestion("Remover Livro", "Deseja remover completamente ou diminuir a quantidade?")
            if prmpt_cfrm=="yes":
                self.lvr_df = self.lvr_df[self.lvr_df["Nome"]!=to_rm_lvr]
                messagebox.showinfo("Remover Livro", f"Livro '{to_rm_lvr}' removido completamente.")
            else:
                rm_lvr_qtd=simpledialog.askinteger("Remover Livro", "Quantidade a ser removida:")
                lvr_pos= self.lvr_df.index[self.lvr_df["Nome"]==to_rm_lvr].tolist()[0]
                self.lvr_df.at[index, "Quantidade"]-=rm_lvr_qtd
                messagebox.showinfo("Remover Livro", f"Quantidade de '{to_rm_lvr}' diminuída.")
        else:
            messagebox.showerror("Remover Livro", "Livro não encontrado.")
    def emp_lvr(self):
        messagebox.showinfo("Em construção","Função ainda será implementada")
    def dev_lvr(self):
        messagebox.showinfo("Em construção","Função ainda será implementada")
    def mais_emp(self):
        cnt_emp=self.emp_df["ID do Livro"].value_counts()
        if not cnt_emp.empty:
            mais_emp_id=cnt_emp.index[:5]
            mais_emp_nm=self.lvr_df[self.lvr_df["ID"].isin(mais_emp_id)]["Nome"].tolist()
            plt.pie(cnt_emp[:5],labels=mais_emp_nm)
            plt.title("Livros mais emprestados")
            plt.show()
        else:
            messagebox.showinfo("Livros mais emprestados", "Nenhum livro foi emprestado ainda.")
    def frq_clnt(self):
        cnt_usr=self.emp_df["ID do Usuário"].value_counts()
        if not cnt_usr.empty:
            frq_clnt_id=cnt_usr.index[:5]
            frq_clnt_nm=self.usr_df[self.usr_df["ID"].isin(frequent_user_ids)]["Nome"].tolist()
            fig,ax=plt.subplots()
            ax.bar(frq_clnt_nm,cnt_usr[:5])
            ax.set_ylabel('Quantidade')
            ax.set_title('Usuários mais frequentes')
            plt.show()
        else:
            messagebox.showinfo("Usuários mais frequentes", "Nenhum usuário fez empréstimo ainda.")
    def rel_emp(self):
        lvr_dsp=self.lvr_df["Quantidade"].sum()
        lvr_emp=len(self.emp_df)
        plt.pie([lvr_dps,lvr_emp],labels=["Disponíveis", "Emprestados"])
        plt.title("Status dos Empréstimos")
        plt.show()   
if __name__ == "__main__":
    base=tk.Tk()
    app=auth(base)
    base.mainloop()
