import math
from typing import Optional
from nicegui import ui

from models import Book, BookState, UserBook

from views.components.core import submit_button

def book_card(book: Book) -> None:
    with ui.card().on('click', lambda: book_dialog(book=book)).classes('p-0 w-full h-56 sm:h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer'):
        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')
            if book.genres:
                genres = book.genres.split(", ")
                end_idx = min(3, len(genres))
                with ui.row().classes('mt-2'):
                    for genre in genres[0:end_idx]:
                        ui.badge(genre.title()).classes('p-1.75').props('rounded')

@ui.refreshable
def render_books(books: list, page: int = 1, books_per_page: int = 10) -> None:
    total_books = len(books)
    total_pages = max(1, math.ceil(total_books / books_per_page))

    page = min(page, total_pages)

    start_idx = (page - 1) * books_per_page
    end_idx = start_idx + books_per_page

    books_for_current_page = books[start_idx:end_idx]

    with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-10 pt-0'):
        for book in books_for_current_page:
            book_card(book=book)

    if total_pages > 1:
        with ui.row().classes('w-full justify-center mt-8 mb-2'):
            ui.pagination(
                min=1,
                max=total_pages,
                value=page,
                on_change=lambda e: render_books.refresh(books=books, page=e.value, books_per_page=books_per_page)
            ).props('rounded color=slate-7')

def render_info_view(book: Book, is_on_shelf: bool, start_on_form: bool, on_switch_to_form: callable, on_switch_to_form_edit: callable) -> None:
    with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
        with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
            ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-cover rounded-lg shadow-md')

        with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
            ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
            ui.label(book.author).classes('text-lg text-slate-500 font-medium')

            if book.genres:
                genres = book.genres.split(", ")
                with ui.row().classes('mt-2 gap-2'):
                    for genre in genres[0:3]:
                        ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')

            ui.space()

            ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

            if start_on_form:
                submit_button(text="Back to your info", on_click=on_switch_to_form).classes('w-full sm:w-auto mt-1 py-2 px-6 rounded-lg shadow-sm font-bold')
            elif is_on_shelf:
                submit_button(text="✓ In shelf", on_click=lambda: ui.notify("Adding book")).classes('w-full sm:w-auto mt-1 py-2 px-6 rounded-lg shadow-sm font-bold').tooltip("Edit book in shelf")
            else:
                submit_button(text="+ Add book", on_click=on_switch_to_form_edit).classes('w-full sm:w-auto mt-1 py-2 px-6 rounded-lg shadow-sm font-bold')

    ui.label("Book info:").classes('font-bold text-slate-800 mt-4 text-lg')

    with ui.scroll_area().classes('w-full flex-grow h-48 sm:h-56 pr-4'):
        ui.label(book.description).classes('text-slate-600 leading-relaxed text-justify')

def render_form_view(book: Book, user_book: Optional[UserBook], on_switch_to_info: callable, on_switch_to_form_edit: callable) -> None:
    with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
            with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
                ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-cover rounded-lg shadow-md')
    
            with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
                ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                ui.label(book.author).classes('text-lg text-slate-500 font-medium')
    
                if book.genres:
                    genres = book.genres.split(", ")
                    with ui.row().classes('mt-2 gap-2'):
                        for genre in genres[0:3]:
                            ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')
    
                ui.space()
    
                ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

                if user_book.rating:
                    ui.label(f"{user_book.rating}/10").classes('text-xl text-slate-400 mt-2')

                if user_book:
                    with ui.row().classes('mt-2 gap-2'):
                        ui.badge(user_book.state.value.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')

                with ui.row().classes('w-full items-center justify-between mb-2 mt-2'):
                    submit_button(text="Edit info", on_click=on_switch_to_form_edit).classes('flex-1 sm:w-auto py-2 px-6 rounded-lg shadow-sm font-bold')
                    ui.button(icon='info', on_click=on_switch_to_info).props('flat round color=slate-500').tooltip('See book info')

    ui.label("Your reading info:").classes('font-bold text-slate-800 mt-4 text-lg')
    
    with ui.scroll_area().classes('w-full flex-grow h-48 sm:h-56 pr-4'):
        with ui.row().classes('w-full gap-4'):
            ui.label(user_book.start_date).classes('text-slate-600 leading-relaxed text-justify')
            ui.label(user_book.end_date).classes('text-slate-600 leading-relaxed text-justify')

        ui.label(user_book.note).classes('text-slate-600 leading-relaxed text-justify')
                    

def render_form_edit_view(book: Book, user_book: Optional[UserBook], start_on_form: bool, on_save: callable, on_switch_to_info: callable, on_switch_to_form: callable) -> None:
    with ui.row().classes('w-full items-center justify-between mb-2'):
        ui.label("Edit Shelf Details" if user_book else "Add to Shelf").classes('text-2xl font-bold text-slate-800')

    with ui.scroll_area().classes('w-full flex-grow h-[60vh] pr-4'):
        with ui.column().classes('w-full gap-4 pb-4'):
            with ui.row().classes('items-center gap-4 w-full bg-slate-50 p-3 rounded-lg'):
                ui.image(book.cover_url).classes('w-12 h-16 object-cover rounded shadow-sm')
                ui.label(book.title).classes('font-semibold text-slate-700 line-clamp-2 flex-1')

            state_select = ui.select(
                options={state: state.value for state in BookState},
                value=user_book.state if user_book else BookState.WISHED,
                label='Book State *'
            ).classes('w-full')

            with ui.row().classes('w-full gap-4'):
                start_date_input = ui.input(
                    'Start Date', 
                    value=user_book.start_date if user_book else ''
                ).props('type=date').classes('flex-1')
                
                end_date_input = ui.input(
                    'End Date', 
                    value=user_book.end_date if user_book else ''
                ).props('type=date').classes('flex-1')  

            rating_input = ui.number(
                'Rating', 
                value=user_book.rating if user_book else None, 
                min=0, max=10
            ).props('clearable').classes('w-full')
            
            note_input = ui.textarea(
                'Note', 
                value=user_book.note if user_book else ''
            ).classes('w-full')

            def handle_submit():
                user_book_data = {
                    'book_id': book.id,
                    'state': state_select.value,
                    'start_date': start_date_input.value or None,
                    'end_date': end_date_input.value or None,
                    'rating': rating_input.value,
                    'note': note_input.value
                }
                on_save(user_book_data)

            submit_button(
                text="Save changes" if user_book else "Save in my shelf", 
                on_click=handle_submit
            ).classes('w-full mt-4 py-2 rounded-lg shadow-sm font-bold')

def book_dialog(book: Book, user_book: Optional[UserBook] = None, start_on_form: bool = False, on_save_user_book: callable = None) -> None:
    is_on_shelf = user_book is not None
    initial_state = "form" if start_on_form else "info"

    with ui.dialog().classes('items-end sm:items-center !mb-0') as dialog:
        with ui.card().classes('w-full sm:max-w-3xl !pb-0 p-6 flex flex-col gap-4 '
            '!mb-0 mt-auto sm:!my-auto max-h-[95vh] sm:max-h-[85vh] '
            'rounded-t-3xl sm:rounded-2xl rounded-b-3xl sm:rounded-b-2xl'):

            @ui.refreshable
            def dynamic_dialog_content(state: str) -> None:
                if state == 'info':
                    render_info_view(
                        book=book,
                        is_on_shelf=is_on_shelf,
                        start_on_form=start_on_form,
                        on_switch_to_form=lambda: dynamic_dialog_content.refresh(state='form'),
                        on_switch_to_form_edit=lambda: dynamic_dialog_content.refresh(state='form_edit')
                    )
                elif state == 'form':
                    render_form_view(
                        book=book,
                        user_book=user_book,
                        on_switch_to_info=lambda: dynamic_dialog_content.refresh(state='info'),
                        on_switch_to_form_edit=lambda: dynamic_dialog_content.refresh(state='form_edit')
                    )
                elif state == 'form_edit':
                    def handle_save(user_book_data):
                        ui.notify("Book data updated successfully!", type='positive')
                        dialog.close()

                    render_form_edit_view(
                        book=book,
                        user_book=user_book,
                        start_on_form=start_on_form,
                        on_save=handle_save,
                        on_switch_to_info=lambda: dynamic_dialog_content.refresh(state='info'),
                        on_switch_to_form=lambda: dynamic_dialog_content.refresh(state='form')
                    )

            dynamic_dialog_content(state=initial_state)

    dialog.open()