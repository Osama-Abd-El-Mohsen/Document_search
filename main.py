import flet as ft
import pandas as pd
data = pd.read_csv('assets/01_edited.csv',encoding='utf-8', usecols=['Document No.', 'Document Title','Doc.Type'])

unique_doc_type = data['Doc.Type'].unique()
title_list = []
no_list = []
cat_list = []


def search(col, search_word: str,cat:str):
    if col['Doc.Type'] == cat :
        if search_word.strip().lower() in str(col['Document Title']).lower():
            title_list.append(str(col['Document Title']))
            no_list.append(str(col['Document No.']))
            cat_list.append(str(col['Doc.Type']))
    elif cat == 'All':
        if search_word.strip().lower() in str(col['Document Title']).lower():
            title_list.append(str(col['Document Title']))
            no_list.append(str(col['Document No.']))
            cat_list.append(str(col['Doc.Type']))


def highlight_text(text, search_word):
    search_word = search_word.strip()
    if not search_word:
        return ft.Text(text)  #
    lower_text = text.lower()
    lower_search = search_word.lower()
    spans = []
    start = 0
    while start < len(lower_text):
        index = lower_text.find(lower_search, start)
        if index == -1:
            spans.append(ft.TextSpan(text[start:]))  
            break
        if index > start:
            spans.append(ft.TextSpan(text[start:index]))  
        spans.append(ft.TextSpan(text[index:index + len(search_word)], ft.TextStyle(color='#000000',bgcolor="yellow", weight=ft.FontWeight.BOLD)))  # Highlighted word
        start = index + len(search_word)
    return ft.Text(spans=spans)


def main(page: ft.Page):
    index_list = []
    page.bgcolor= '#1c1f26'

    # def on_select(args):
        # print(f"row select : {args.control.cells[1].content.value}"),
    
    def save_as_CSV(args):
        try :
            df = pd.DataFrame({'index':index_list,'category':cat_list,'Document No.': no_list, 'Document Title': title_list})
            df.to_csv('result.csv', index=False)
            page.open(ft.SnackBar(ft.Text(f"'result.csv' saved successfully", color='#fcfffd'),bgcolor='#16181d'))
        except : page.open(ft.SnackBar(ft.Text(f"Error saving file", color='#fcfffd'),bgcolor='#16181d'))

    def save_as_TXT(args):
        try:
            df = pd.DataFrame({'index':index_list,'category':cat_list,'Document No.': no_list, 'Document Title': title_list})
            df.to_csv('result.txt', index=False)
            page.open(ft.SnackBar(ft.Text(f"'result.txt' saved successfully", color='#fcfffd'),bgcolor='#16181d'))
        except : page.open(ft.SnackBar(ft.Text(f"Error saving file", color='#fcfffd'),bgcolor='#16181d'))

    def drop_menu_on_change(args):
        drop_down_menu.border_color = '#a0cafd'


    def do_search(args):
        if drop_down_menu.value == None:
            drop_down_menu.border_color = 'red'
            page.open(ft.SnackBar(ft.Text(f"please select category", color='#fcfffd'),bgcolor='#16181d'))
            page.update()

        else :
            drop_down_menu.border_color = '#a0cafd'
            search_text = search_field.value
            title_list.clear()  
            no_list.clear()
            cat_list.clear()
            index_list.clear()
            data.apply(lambda row: search(row, search_text,drop_down_menu.value), axis=1)
            index_list.extend(range(1,len(title_list)+1))

            filtered_rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(index))),
                        ft.DataCell(ft.Text(str(cat_val))),
                        ft.DataCell(ft.Text(str(no))),
                        ft.DataCell(highlight_text(title, search_text)),  
                    ],
                    # on_select_changed=on_select,
                )
                for index,cat_val, no, title in zip(index_list,cat_list, no_list, title_list)
            ]

            table.rows = filtered_rows
            result_text.value = f'Found {len(title_list)} Item'
            page.update()
            page.open(ft.SnackBar(ft.Text(f"search finished Found {len(title_list)} Item", color='#fcfffd'),bgcolor='#16181d'))

    img = ft.Image(
        src=f"assets/icon.png",
        width=100,
        height=100,
        fit=ft.ImageFit.CONTAIN,
    )

    drop_down_menu = ft.DropdownM2(
            label="Category",
            hint_text="Choose The Category",
            options=[
                ft.dropdownm2.Option('All'),  
                *[ft.dropdownm2.Option(x) for x in unique_doc_type] 
            ],
            autofocus=True,
            on_change= drop_menu_on_change
        )

    search_field = ft.TextField(
        hint_text="Enter Search Word",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        height=50,
        label="Search here",
        border_radius = 80,
        text_size=20,
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Index"), numeric=True),
            ft.DataColumn(ft.Text("Categoy")),
            ft.DataColumn(ft.Text("Document No.")),
            ft.DataColumn(ft.Text("Document Title")),
        ],
        rows=[],
        border_radius=20,
        bgcolor='#16181d',
        heading_text_style = {'color':"#a0cafd",'size':20,'font_family':"poppins"},
        data_text_style = {'color':"#fcfffd",'size':16,'font_family':"poppins"},
        divider_thickness = 3,

    )

    table_container = ft.Container(
        content=ft.Column(
            [table],
            scroll=ft.ScrollMode.AUTO 
        ),
        expand=True
    )

    search_button = ft.CupertinoFilledButton(
        "Search",
        on_click=do_search,
        icon=ft.Icons.SEARCH,
        icon_color = '#000000',
        height=50)
    
    print_button = ft.CupertinoFilledButton(
        content=ft.Text("print",size=18,font_family='poppins'),
        on_click=print,
        )
    
    save_as_csv_button = ft.CupertinoFilledButton(
        content=ft.Text("Save As CSV",size=18,font_family='poppins'),
        on_click=save_as_CSV,
        )
    
    save_as_txt_button = ft.CupertinoFilledButton(
        content=ft.Text("Save As TXT",size=18,font_family='poppins'),
        on_click=save_as_TXT,
        )
    

    result_text = ft.Text(f'Found ــ Item',size = 16,font_family="poppins")

    page.add(ft.Row([img,drop_down_menu,search_field, search_button,result_text]))
    page.add(table_container)
    page.add(ft.Row([save_as_csv_button,save_as_txt_button],alignment=ft.MainAxisAlignment.CENTER))


ft.app(target=main,assets_dir="assets")
