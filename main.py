import flet as ft
import pandas as pd

data = pd.read_csv('assets/01_edited.csv', encoding='cp1252', usecols=['Document No.', 'Document Title'])

title_list = []
no_list = []


def search(col, search_word: str):
    if search_word.strip().lower() in str(col['Document Title']).lower():
        title_list.append(str(col['Document Title']))
        no_list.append(str(col['Document No.']))


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

    def do_search(args):
        search_text = search_field.value
        title_list.clear()  
        no_list.clear()
        index_list.clear()

        data.apply(lambda row: search(row, search_text), axis=1)
        index_list.extend(range(len(title_list)))

        filtered_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(index))),
                    ft.DataCell(ft.Text(str(no))),
                    ft.DataCell(highlight_text(title, search_text)),  
                ],
                # on_select_changed=on_select,
            )
            for index, no, title in zip(index_list, no_list, title_list)
        ]

        table.rows = filtered_rows
        result_text.value = f'Found {len(title_list)-1} Item'
        page.update()

        df = pd.DataFrame({'index':index_list,'Document No.': no_list, 'Document Title': title_list})
        df.to_csv('result.csv', index=False)

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

    result_text = ft.Text(f'Found ــ Item',size = 16,font_family="poppins")

    page.add(ft.Row([search_field, search_button,result_text])
)
    page.add(table_container)


ft.app(target=main,assets_dir="assets")
