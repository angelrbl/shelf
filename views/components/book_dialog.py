from nicegui import ui
from datetime import date
from typing import Optional

from models import Book, UserBook, BookState
from services import get_user_book, remove_book, get_user_shelf, add_book, get_user_book_by_google_id

from views.theme import STATE_COLORS
from views.components.core import submit_button, icon_button, user_select

def render_info_view(book: Book, is_on_shelf: bool, start_on_form: bool, on_switch_to_form: callable, on_switch_to_form_edit: callable, on_delete: callable, close_dialog: callable) -> None:
    with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
        with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
            ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-contain rounded-lg shadow-md')

        with ui.column().classes('col-span-1 sm:col-span-2 w-full sm:h-full justify-between gap-1'):
            with ui.row().classes('w-full justify-between items-start flex-nowrap'):
                ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                icon_button(icon="close", color="slate-500", tooltip="Close", on_click=close_dialog)
            ui.label(book.author).classes('text-lg text-slate-500 font-medium')

            with ui.row().classes('w-full justify-between pr-4 mt-2 mb-4 items-center'):
                if book.genres:
                    genres = book.genres.split(", ")
                    with ui.row().classes('mt-2 gap-2'):
                        for genre in genres[0:3]:
                            ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')
                ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

            ui.separator()
            ui.space()

            if start_on_form:
                submit_button(text="Go back", on_click=on_switch_to_form).classes('w-full sm:w-full mt-1 py-2 px-6 rounded-lg shadow-sm font-bold')
            elif is_on_shelf:
                with ui.row().classes('gap-5 w-full mt-1 pr-2'):
                    submit_button(text="✓ In shelf", on_click=on_switch_to_form).classes('flex-1 py-2 px-6 rounded-lg shadow-sm font-bold').tooltip("See book in shelf")
                    icon_button(icon='delete', on_click=on_delete, color="red-500", tooltip="Remove from shelf")
            else:
                submit_button(text="+ Add book", on_click=on_switch_to_form_edit).classes('w-full sm:w-full mt-1 py-2 px-6 rounded-lg shadow-sm font-bold')

    
    with ui.column().classes('bg-slate-50 rounded-xl p-4 mb-4 w-full mt-4 border border-slate-100'):
        ui.label("Book info:").classes('font-bold text-slate-800 text-lg')

        with ui.column().classes('w-full flex-grow h-48 sm:h-56 pr-4 overflow-y-auto'):
            desc = book.description if book.description else "No description available for this book."
            ui.label(desc).classes('text-slate-600 leading-relaxed text-justify break-words')

def render_form_view(book: Book, user_book: Optional[UserBook], on_switch_to_info: callable, on_switch_to_form_edit: callable, on_delete: callable, close_dialog: callable) -> None:
    with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
            with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
                ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-contain rounded-lg shadow-md')
    
            with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
                with ui.row().classes('w-full justify-between items-start flex-nowrap'):
                    ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                    icon_button(icon="close", color="slate-500", tooltip="Close", on_click=close_dialog)
                ui.label(book.author).classes('text-lg text-slate-500 font-medium')

                with ui.row().classes('w-full justify-between pr-4 mt-2 mb-4 items-center'):
                    if book.genres:
                        genres = book.genres.split(", ")
                        with ui.row().classes('mt-2 gap-2'):
                            for genre in genres[0:3]:
                                ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')
                    ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

                ui.separator()
                ui.space()
    
                with ui.row().classes('justify-between w-full items-end gap-5'):
                    current_state = user_book.state
                    color_classes = STATE_COLORS.get(current_state, "bg-slate-100 text-slate-700")

                    ui.badge(user_book.state.value.title()).classes(f'{color_classes} px-4 py-1.5 text-sm font-semibold').props('rounded')

                    if user_book.rating:
                        ui.label(f"{float(user_book.rating):g}/10").classes('text-5xl font-semibold text-slate-600 pr-2')

                with ui.row().classes('w-full items-center justify-between mt-1'):
                    submit_button(text="Edit info", on_click=on_switch_to_form_edit).classes('flex-1 sm:w-auto py-2 px-6 rounded-lg shadow-sm font-bold')

                    with ui.row().classes('gap-2'):
                        icon_button(icon='info', on_click=on_switch_to_info, color="slate-500", tooltip="See book info")
                        icon_button(icon='delete', on_click=on_delete, color="red-500", tooltip="Remove from shelf")

    with ui.column().classes('w-full mt-4 h-48 sm:h-56 pr-4 overflow-y-auto'):
        if user_book and (user_book.start_date or user_book.end_date or user_book.note):
            with ui.column().classes('bg-slate-50 rounded-xl p-4 w-full border border-slate-100'):

                if user_book.start_date or user_book.end_date:
                    border_class = 'border-b border-slate-200 pb-3 mb-2' if user_book.note else ''

                    with ui.row().classes(f'w-full items-center justify-center gap-6 {border_class}'):
        
                        if user_book.start_date:
                            with ui.row().classes('items-center gap-2 text-slate-500'):
                                ui.icon('calendar_today').classes('text-lg')
                                ui.label(f"Started: {user_book.start_date}").classes('text-sm font-medium')

                        if user_book.end_date:
                            with ui.row().classes('items-center gap-2 text-slate-500'):
                                ui.icon('flag').classes('text-lg')
                                ui.label(f"Finished: {user_book.end_date}").classes('text-sm font-medium')

                if user_book.note:
                    margin_class = 'mt-2' if (user_book.start_date or user_book.end_date) else ''

                    with ui.column().classes(f'w-full gap-1 {margin_class}'):
                        ui.icon('format_quote').classes('text-3xl text-slate-300 -mb-2 -ml-1')
                        ui.label(user_book.note).classes('text-slate-700 italic leading-relaxed text-justify text-base px-2 break-words')

def render_form_edit_view(book: Book, user_book: Optional[UserBook], on_save: callable, on_switch_to_info: callable) -> None:
    with ui.row().classes('w-full items-center justify-between mb-2'):
        ui.label("Edit details" if user_book else "Add to Shelf").classes('text-2xl font-bold text-slate-800')

    with ui.column().classes('w-full flex-grow sm:max-h-[70dvh] h-[60dvh] sm:h-[50dvh] pr-4 overflow-y-auto'):
        with ui.column().classes('w-full gap-4 pb-4'):
            with ui.row().classes('items-center gap-4 w-full bg-slate-50 p-3 rounded-lg justify-between'):
                with ui.row().classes("items-center flex-1"):
                    ui.image(book.cover_url).classes('w-12 h-16 object-contain rounded shadow-sm')
                    ui.label(book.title).classes('font-semibold text-slate-700 line-clamp-2 flex-1')
                icon_button(icon='info', on_click=on_switch_to_info, color="slate-500", tooltip="See book info")

            with ui.row().classes('w-full gap-4 flex-col sm:flex-row'):
                state_select = user_select(
                    options={state: state.value.title() for state in BookState},
                    value=user_book.state if user_book else BookState.WISHED,
                    label='Book State *',
                    icon='bookmark'
                ).props('outlined color=slate-700').classes('sm:flex-1')

                with ui.number(
                    'Rating (0-10)', 
                    value=user_book.rating if user_book else None, 
                    min=0, max=10, step=0.1, format='%g'
                ).props('outlined color=slate-700 clearable').classes('w-full sm:w-1/3') as rating_input:
                    with rating_input.add_slot('prepend'):
                        ui.icon('star').classes('text-slate-500 text-xl')

            with ui.row().classes('w-full gap-4'):
                start_date_input = ui.input(
                    'Start Date', 
                    value=date.strftime(user_book.start_date, '%Y-%m-%d') if user_book and user_book.start_date else ''
                ).props('type=date outlined color=slate-700').classes('flex-1')
                
                end_date_input = ui.input(
                    'End Date', 
                    value=date.strftime(user_book.end_date, '%Y-%m-%d') if user_book and user_book.end_date else ''
                ).props('type=date outlined color=slate-700').classes('flex-1')  

            with ui.textarea(
                'Your thoughts...', 
                value=user_book.note if user_book else ''
            ).props('outlined color=slate-700 autogrow').classes('w-full') as note_input:
                with note_input.add_slot('prepend'):
                    ui.icon('edit_note').classes('text-slate-500 text-xl pt-2')

            def handle_submit():
                user_book_data = {
                    'book': book,
                    'google_book_id': book.google_book_id,
                    'state': state_select.value,
                    'start_date': date.strptime(start_date_input.value, '%Y-%m-%d') if start_date_input.value else None,
                    'end_date': date.strptime(end_date_input.value, '%Y-%m-%d') if end_date_input.value else None,
                    'rating': rating_input.value,
                    'note': note_input.value
                }
                on_save(user_book_data)

            submit_button(
                text="Save changes" if user_book else "Save in my shelf", 
                on_click=handle_submit
            ).classes('w-full mt-4 py-2 rounded-lg shadow-sm font-bold')

def render_visitor_view(
        book: Book,
        profile_user_book: UserBook,
        current_user_book: Optional[UserBook],
        on_see_in_shelf: callable,
        on_switch_to_info: callable,
        on_switch_to_form_edit: callable,
        close_dialog: callable
    ) -> None:
    with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
        with ui.column().classes('col-span-1 w-full items-center sm:items-start'):
            ui.image(book.cover_url).classes('w-36 sm:w-full h-52 sm:h-72 object-contain rounded-lg shadow-md')

        with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
            with ui.row().classes('w-full justify-between items-start flex-nowrap'):
                ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
                icon_button(icon="close", color="slate-500", tooltip="Close", on_click=close_dialog)
            ui.label(book.author).classes('text-lg text-slate-500 font-medium')

            with ui.row().classes('w-full justify-between pr-4 mt-2 mb-4 items-center'):
                if book.genres:
                    genres = book.genres.split(", ")
                    with ui.row().classes('mt-2 gap-2'):
                        for genre in genres[0:3]:
                            ui.badge(genre.title()).classes('bg-slate-100 px-2.5 py-1 font-semibold').props('rounded')
                ui.label(f"{book.page_count} pages").classes('text-sm text-slate-400 mt-2')

            ui.separator()
            ui.space()

            with ui.row().classes('justify-between w-full items-end gap-5'):
                current_state = profile_user_book.state
                color_classes = STATE_COLORS.get(current_state, "bg-slate-100 text-slate-700")

                ui.badge(profile_user_book.state.value.title()).classes(f'{color_classes} px-4 py-1.5 text-sm font-semibold').props('rounded')

                if profile_user_book.rating:
                    ui.label(f"{float(profile_user_book.rating):g}/10").classes('text-5xl font-semibold text-slate-600 pr-2')

            with ui.row().classes('w-full items-center justify-between mt-1'):
                if current_user_book:
                    with ui.row().classes('gap-5 w-full mt-1 pr-2'):
                        submit_button(text="✓ In shelf", on_click=on_see_in_shelf).classes('flex-1 py-2 px-6 rounded-lg shadow-sm font-bold').tooltip("See book in shelf")
                        icon_button(icon='info', on_click=on_switch_to_info, color="slate-500", tooltip="See book info")
                else:
                    with ui.row().classes('gap-5 w-full mt-1 pr-2'):
                        submit_button(text="+ Add book", on_click=on_switch_to_form_edit).classes('flex-1 py-2 px-6 rounded-lg shadow-sm font-bold')
                        icon_button(icon='info', on_click=on_switch_to_info, color="slate-500", tooltip="See book info")

    with ui.column().classes('w-full flex-grow h-48 sm:h-56 pr-4 overflow-y-auto'):
            if profile_user_book.start_date or profile_user_book.end_date or profile_user_book.note:

                if profile_user_book.start_date or profile_user_book.end_date:
                    with ui.row().classes('w-full items-center justify-center gap-6 border-b border-slate-200 pb-3 mb-2'):
        
                        if profile_user_book.start_date:
                            with ui.row().classes('items-center gap-2 text-slate-500'):
                                ui.icon('calendar_today').classes('text-lg')
                                ui.label(f"Started: {profile_user_book.start_date}").classes('text-sm font-medium')

                        if profile_user_book.end_date:
                            with ui.row().classes('items-center gap-2 text-slate-500'):
                                ui.icon('flag').classes('text-lg')
                                ui.label(f"Finished: {profile_user_book.end_date}").classes('text-sm font-medium')

                if profile_user_book.note:
                    with ui.column().classes('w-full gap-1 mt-2'):
                        ui.icon('format_quote').classes('text-3xl text-slate-300 -mb-2 -ml-1')
                        ui.label(profile_user_book.note).classes('text-slate-700 italic leading-relaxed text-justify text-base px-2')

def book_dialog(
        profile_user_id: int,
        book: Book,
        profile_user_book: Optional[UserBook] = None,
        start_on_form: bool = False,
        on_close: callable | None = None,
        is_owner: bool = True,
        current_user_id: int | None = None
    ) -> None:

    if not current_user_id:
        current_user_id = profile_user_id
    
    if not profile_user_book:
        profile_user_book = get_user_book(user_id=profile_user_id, book_id=book.id)

    current_user_book = get_user_book(user_id=current_user_id, book_id=book.id)

    if is_owner:
        initial_state = "form" if start_on_form else "info"
    else:
        initial_state = "visitor"

    with ui.dialog().classes('items-end sm:items-center !mb-0') as dialog:

        with ui.card().classes('book-dialog-card w-full sm:max-w-3xl !pb-0 p-6 flex flex-col gap-4 '
        '!mb-0 mt-auto sm:!my-auto max-h-[95dvh] sm:max-h-[85dvh] overflow-y-auto '
        'rounded-t-3xl sm:rounded-2xl rounded-b-3xl sm:rounded-b-2xl overflow-y-auto overflow-x-hidden isolate'):

            @ui.refreshable
            def dynamic_dialog_content(state: str, user_book: Optional[UserBook], current_user_book_data: Optional[UserBook]) -> None:
                current_book = user_book.book if user_book else book

                def handle_delete():
                    remove_book(user_id=current_user_id, book_id=current_book.id)
                    ui.notify("Book removed from your shelf.", type='positive')
                    dialog.close()
                    if start_on_form:
                        from views.components.shelf import render_shelf
                        user_shelf = get_user_shelf(user_id=current_user_id)
                        render_shelf.refresh(user_shelf=user_shelf)

                        if on_close:
                            dialog.on('hide', on_close)

                    else:
                        from views.components.books import render_books
                        render_books.refresh()
                        
                if state == 'info':
                    has_book_in_my_shelf = current_user_book_data is not None

                    render_info_view(
                        book=current_book,
                        is_on_shelf=has_book_in_my_shelf,
                        start_on_form=start_on_form,
                        on_switch_to_form=lambda: dynamic_dialog_content.refresh(state=('form' if is_owner else 'visitor'), user_book=user_book, current_user_book_data=current_user_book_data),
                        on_switch_to_form_edit=lambda: dynamic_dialog_content.refresh(state='form_edit', user_book=user_book, current_user_book_data=current_user_book_data),
                        on_delete=handle_delete,
                        close_dialog=dialog.close
                    )
                elif state == 'form':
                    book_to_show = user_book if is_owner else current_user_book_data

                    render_form_view(
                        book=current_book,
                        user_book=book_to_show,
                        on_switch_to_info=lambda: dynamic_dialog_content.refresh(state='info', user_book=user_book, current_user_book_data=current_user_book_data),
                        on_switch_to_form_edit=lambda: dynamic_dialog_content.refresh(state='form_edit', user_book=user_book, current_user_book_data=current_user_book_data),
                        on_delete=handle_delete,
                        close_dialog=dialog.close
                    )
                elif state == 'form_edit':
                    def handle_save(user_book_data):
                        try:
                            add_book(
                                user_id=current_user_id,
                                book=user_book_data.get("book"),
                                state=user_book_data.get("state"),
                                start_date=user_book_data.get("start_date"),
                                end_date=user_book_data.get("end_date"),
                                rating=user_book_data.get("rating"),
                                note=user_book_data.get("note")
                            )

                            updated_user_book = get_user_book_by_google_id(user_id=current_user_id, google_book_id=user_book_data.get("google_book_id"))

                            ui.notify("Book data updated successfully!", type='positive')
                            dynamic_dialog_content.refresh(
                                state='form', 
                                user_book=updated_user_book, 
                                current_user_book_data=updated_user_book
                            )

                            if on_close:
                                dialog.on('hide', on_close)

                        except ValueError as err:
                            ui.notify("End date can't be early than start date.", type='negative')

                    book_to_edit = user_book if is_owner else current_user_book_data

                    render_form_edit_view(
                        book=current_book,
                        user_book=book_to_edit,
                        on_save=handle_save,
                        on_switch_to_info=lambda: dynamic_dialog_content.refresh(state='info', user_book=user_book, current_user_book_data=current_user_book_data),
                    )
                elif state == 'visitor':
                    render_visitor_view(
                        book=book,
                        profile_user_book=user_book,
                        current_user_book=current_user_book_data,
                        on_switch_to_info=lambda: dynamic_dialog_content.refresh(state='info', user_book=user_book, current_user_book_data=current_user_book_data),
                        on_switch_to_form_edit=lambda: dynamic_dialog_content.refresh(state='form_edit', user_book=user_book, current_user_book_data=current_user_book_data),
                        on_see_in_shelf=lambda: dynamic_dialog_content.refresh(state='form', user_book=user_book, current_user_book_data=current_user_book_data),
                        close_dialog=dialog.close
                    )

            dynamic_dialog_content(state=initial_state, user_book=profile_user_book, current_user_book_data=current_user_book)

    dialog.open()