import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

DATA_FILE = "produtos.json"

def load_products():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

def refresh_product_list():
    listbox_products.delete(0, tk.END)
    for i, product in enumerate(products):
        listbox_products.insert(tk.END, f"{i+1}. {product['name']} - R${product['price']}")

def select_product(event):
    selection = listbox_products.curselection()
    if not selection:
        return
    index = selection[0]
    product = products[index]

    entry_name.delete(0, tk.END)
    entry_name.insert(0, product["name"])

    entry_price.delete(0, tk.END)
    entry_price.insert(0, product["price"])

    entry_description.delete("1.0", tk.END)
    entry_description.insert("1.0", product.get("description", ""))

    combo_tag.set(product.get("tag", "Nenhuma"))

    selected_image.set(product.get("image", ""))

def add_product():
    name = entry_name.get()
    price = entry_price.get()
    description = entry_description.get("1.0", tk.END).strip()
    tag = combo_tag.get()
    image = selected_image.get()

    if not name or not price or not image:
        messagebox.showerror("Erro", "Nome, preço e imagem são obrigatórios.")
        return

    products.append({
        "name": name,
        "price": price,
        "description": description,
        "tag": tag,
        "image": image
    })
    save_products(products)
    refresh_product_list()
    clear_fields()
    messagebox.showinfo("Sucesso", f"Produto '{name}' adicionado!")

def update_product():
    selection = listbox_products.curselection()
    if not selection:
        messagebox.showerror("Erro", "Selecione um produto para atualizar.")
        return

    index = selection[0]
    products[index] = {
        "name": entry_name.get(),
        "price": entry_price.get(),
        "description": entry_description.get("1.0", tk.END).strip(),
        "tag": combo_tag.get(),
        "image": selected_image.get()
    }
    save_products(products)
    refresh_product_list()
    clear_fields()
    messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

def delete_product():
    selection = listbox_products.curselection()
    if not selection:
        messagebox.showerror("Erro", "Selecione um produto para remover.")
        return
    index = selection[0]
    name = products[index]["name"]
    del products[index]
    save_products(products)
    refresh_product_list()
    clear_fields()
    messagebox.showinfo("Removido", f"Produto '{name}' removido!")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_description.delete("1.0", tk.END)
    combo_tag.set("Nenhuma")
    selected_image.set("")
    listbox_products.selection_clear(0, tk.END)

def select_image():
    file_path = filedialog.askopenfilename(
        title="Selecione a imagem do produto",
        filetypes=[("Arquivos de imagem", "*.jpg *.jpeg *.png *.gif *.webp")]
    )
    if file_path:
        folder = os.path.basename(os.path.dirname(file_path))  # nome da pasta anterior
        name, ext = os.path.splitext(os.path.basename(file_path))  # nome do arquivo e extensão
        result = f"{folder}/{name}{ext}"
        selected_image.set(result)

# Janela principal
root = tk.Tk()
root.title("Cadastro de Produtos - Amigurumis")
root.geometry("600x500")

products = load_products()

# Lista de produtos
frame_list = tk.Frame(root)
frame_list.pack(side="left", fill="y", padx=5, pady=5)

listbox_products = tk.Listbox(frame_list, width=40)
listbox_products.pack(side="left", fill="y")
listbox_products.bind("<<ListboxSelect>>", select_product)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")
listbox_products.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_products.yview)

# Formulário
frame_form = tk.Frame(root)
frame_form.pack(side="right", fill="both", expand=True, padx=5, pady=5)

tk.Label(frame_form, text="Nome do Produto:").pack()
entry_name = tk.Entry(frame_form)
entry_name.pack(fill="x", padx=5)

tk.Label(frame_form, text="Preço:").pack()
entry_price = tk.Entry(frame_form)
entry_price.pack(fill="x", padx=5)

tk.Label(frame_form, text="Descrição:").pack()
entry_description = tk.Text(frame_form, height=4)
entry_description.pack(fill="x", padx=5)

tk.Label(frame_form, text="Tag:").pack()
combo_tag = ttk.Combobox(frame_form, values=["Nenhuma", "Novo", "Promoção", "Edição Limitada"])
combo_tag.set("Nenhuma")
combo_tag.pack(fill="x", padx=5)

tk.Label(frame_form, text="Imagem do Produto:").pack()
selected_image = tk.StringVar()
tk.Button(frame_form, text="Selecionar Imagem", command=select_image).pack(pady=2)
tk.Label(frame_form, textvariable=selected_image, fg="blue").pack()

# Botões de ação
tk.Button(frame_form, text="Adicionar Produto", command=add_product, bg="pink").pack(pady=5)
tk.Button(frame_form, text="Atualizar Produto", command=update_product, bg="lightblue").pack(pady=5)
tk.Button(frame_form, text="Remover Produto", command=delete_product, bg="red", fg="white").pack(pady=5)
tk.Button(frame_form, text="Limpar Campos", command=clear_fields).pack(pady=5)

refresh_product_list()
root.mainloop()
