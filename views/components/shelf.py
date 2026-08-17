import math
from nicegui import ui

from models import UserBook, BookState
from services import get_user_shelf, filter_user_shelf, get_unique_shelf_genres, update_top_shelf_rank

from views.theme import STATE_COLORS
from views.components.core import section_title, user_input, user_select, icon_button
from views.components.book_dialog import book_dialog

def user_book_card(user_book: UserBook, on_click: callable, rank: int | None = None) -> None:
    book = user_book.book

    with ui.card().on("click", on_click).classes('p-0 w-full h-full overflow-hidden shadow-sm hover:shadow-md transition-all rounded-md cursor-pointer flex flex-col'):

        ui.image(book.cover_url).classes('h-24 sm:h-56 w-full object-contain shrink-0')
        with ui.column().classes('p-2.5 sm:p-5 pt-0 gap-1 sm:pt-1 flex-1 justify-between flex flex-col w-full'):
            ui.label(book.title).classes('font-semibold text-sm w-full line-clamp-2')
            ui.label(book.author).classes('text-xs text-slate-500')

            ui.space()
            
            with ui.row().classes('w-full mt-2 justify-between items-center'):
                if not rank:
                    current_state = user_book.state
                    color_classes = STATE_COLORS.get(current_state, "bg-slate-100 text-slate-700")
                    
                    ui.badge(user_book.state.value.title()).classes(f'{color_classes} p-1.75').props('rounded')
                else:
                    ui.label(f"#{rank}").classes("text-bold text-slate-600 text-bold text-xl")
                    
                if user_book.rating:
                    ui.label(f"{user_book.rating}/10").classes("text-bold text-slate-600 text-bold text-lg")


def add_book_card(on_click: callable) -> None:
    with ui.card().on('click', on_click).classes(
        'w-full h-full min-h-[200px] sm:min-h-[300px] items-center justify-center cursor-pointer '
        'bg-transparent shadow-sm hover:shadow-md border border-dashed border-gray-700'
    ):
        ui.label('+ Add Book').classes('text-gray-700')

def render_currently_reading(user_id: int | None = None, currently_reading_books: list[UserBook] | None = None) -> None:
    if not currently_reading_books:
        return

    if not user_id:
        user_id = currently_reading_books[0].user_id

    with ui.column().classes('w-full max-w-4xl mx-auto gap-4 sm:mt-8 px-4'):

        section_title(icon="auto_stories", text="On the nightstand")

        has_multiple_books = len(currently_reading_books) > 1

        carousel_props = 'animated swipeable control-text-color=slate-500'
        if has_multiple_books:
            carousel_props += ' navigation padding'

        with ui.carousel().props(carousel_props).classes('w-full bg-transparent sm:h-[364px] h-[480px]'):
            for user_book in currently_reading_books:

                book = user_book.book

                with ui.carousel_slide(name=book.id):
                    with ui.card().classes('w-full p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-100 bg-white hover:shadow-md transition-all'):
                        with ui.grid().classes('w-full grid-cols-1 sm:grid-cols-3 gap-6 items-stretch'):
                                with ui.column().classes('col-span-1 w-full justify-center items-center'):
                                    (
                                        ui.image(book.cover_url)
                                        .classes('w-32 h-44 sm:w-40 sm:h-56 object-cover rounded-xl shadow-md cursor-pointer hover:shadow-xl transition-all')
                                        .on("click", lambda: book_dialog(user_id=user_id, book=book))
                                    )
                        
                                with ui.column().classes('col-span-1 sm:col-span-2 w-full h-full justify-between gap-1'):
                                    ui.label(book.title).classes('text-2xl sm:text-3xl font-bold leading-tight text-slate-800')
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

                                    if user_book.start_date:
                                        with ui.row().classes('w-full items-center justify-center sm:justify-start gap-2 text-slate-500'):
                                            ui.icon('calendar_today').classes('text-lg')
                                            ui.label(f"Started: {user_book.start_date}").classes('text-sm font-medium')

def render_top_shelf(current_user_id: int, profile_user_id: int, top_shelf: list[UserBook], on_add_book: callable, is_owner: bool=False, max_top_books: int = 5) -> None:
    top_shelf_by_rank = {user_book.top_shelf_rank: user_book for user_book in top_shelf if user_book.top_shelf_rank}

    with ui.column().classes('w-full max-w-4xl mx-auto gap-4 px-4'):

        section_title(icon="emoji_events", text="Top shelf")

        with ui.card().classes('w-full p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-100 bg-white hover:shadow-md transition-all'):
            with ui.row().classes('w-full flex-nowrap overflow-x-auto gap-6 pb-4 pt-4 px-2 snap-x snap-mandatory'):

                for rank in range(1, max_top_books+1):
                    if rank in top_shelf_by_rank:
                        user_book = top_shelf_by_rank[rank]

                        with ui.column().classes('relative w-32 sm:w-40 h-[310px] sm:h-[370px] flex-shrink-0 snap-start ' 
                            'cursor-pointer hover:-translate-y-1 transition-transform duration-300 gap-2'):
                            user_book_card(user_book=user_book, rank=rank, on_click=
                                lambda u_book=user_book: book_dialog(
                                user_id=current_user_id,
                                book=u_book.book,
                                current_user_book=u_book,
                                start_on_form=True,
                                on_close=lambda:render_shelf.refresh(user_shelf=get_user_shelf(user_id=u_book.user_id))),
                            )
                            if is_owner:
                                icon_button(
                                    icon="close", 
                                    color="white", 
                                    on_click=lambda bid=user_book.book_id: ui.notify("a"),
                                    tooltip="Remove book from top shelf"
                                ).classes(
                                    'absolute top-2 right-2 bg-slate-900/60 hover:bg-red-600 '
                                    'text-white rounded-full z-10 p-1 transition-colors shadow-md'
                                ).props('dense flat size=sm')

                    elif is_owner:
                        with ui.column().classes('relative w-32 sm:w-40 h-[310px] sm:h-[370px] flex-shrink-0 snap-start ' 
                            'cursor-pointer hover:-translate-y-1 transition-transform duration-300 gap-2'):
                            add_book_card(on_click=lambda r=rank: render_shelf_search_dialog(user_id=profile_user_id, on_close=on_add_book, initial_state=BookState.READ, rank=r))

@ui.refreshable
def render_shelf(user_shelf: list, page: int = 1, books_per_page: int = 9) -> None:
    total_books = len(user_shelf)
    total_pages = max(1, math.ceil(total_books / books_per_page))

    page = min(page, total_pages)

    start_idx = (page - 1) * books_per_page
    end_idx = start_idx + books_per_page

    books_for_current_page = user_shelf[start_idx:end_idx]

    with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6 p-10 pt-0'):
        for user_book in books_for_current_page:
            user_book_card(user_book=user_book, on_click=lambda u_book=user_book: book_dialog(
                user_id=u_book.user_id,
                book=u_book.book,
                current_user_book=u_book,
                start_on_form=True,
                on_close=lambda:render_shelf.refresh(user_shelf=get_user_shelf(user_id=u_book.user_id))))

        add_book_card(on_click=lambda: ui.navigate.to('/search'))

    if total_pages > 1:
        with ui.row().classes('w-full justify-center mt-8 mb-4'):
            ui.pagination(
                min=1,
                max=total_pages,
                value=page,
                on_change=lambda e: render_shelf.refresh(user_shelf=user_shelf, page=e.value, books_per_page=books_per_page)
            ).props('rounded color=slate-7')

def render_shelf_search_dialog(user_id: int, on_close: callable, rank:int, initial_state: BookState | None = None) -> None:
    user_shelf = get_user_shelf(user_id=user_id)

    def handle_filter_shelf(query: str | None = None, state: BookState | None = None, genre: str | None = None):
        filtered_shelf = filter_user_shelf(shelf=user_shelf, query=query, state=state, genre=genre)
        mini_render_shelf.refresh(user_shelf=filtered_shelf)

    def handle_add_to_top_shelf(user_id: int, book_id: int, rank: int):
        update_top_shelf_rank(user_id=user_id, book_id=book_id, new_top_shelf_rank=rank)
        ui.notify("Book added successfully to top shelf!", type="positive")
        dialog.close()

    with ui.dialog().classes('items-end sm:items-center !mb-0') as dialog:
        with ui.card().classes('w-full sm:max-w-3xl !pb-0 p-6 flex flex-col gap-4 '
            '!mb-0 mt-auto sm:!my-auto max-h-[95vh] sm:max-h-[85vh] '
            'rounded-t-3xl sm:rounded-2xl rounded-b-3xl sm:rounded-b-2xl'):
                with ui.column().classes('w-full gap-3'):
                    with ui.row().classes('w-full items-center justify-between mb-2'):
                        ui.label(f"Select a book").classes('text-2xl font-bold text-slate-700')
                        icon_button(icon="close", color="slate-700", tooltip="Close", on_click=dialog.close)

                    with ui.row().classes('w-full max-w-6xl items-center gap-3 flex-col sm:flex-row'):
                        query = (
                            user_input(label="Search your books", icon="search")
                            .on('keydown.enter', lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value))
                            .on('blur', lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value))
                            .classes("sm:flex-1")
                            .props(remove='outlined')
                        )
            
                        with ui.row().classes('w-full sm:w-auto gap-3 flex-1'):
                            state = user_select(
                                label="State",
                                options={None: "All states", **{state: state.value.title() for state in BookState}},
                                value=initial_state,
                                on_change=lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value),
                                icon="bookmark_border"
                            ).classes(remove="w-full", add="flex-1 sm:w-44")
                            genre = user_select(
                                label="Genre",
                                options={None: "All genres", **{genre.lower(): genre for genre in get_unique_shelf_genres(shelf=user_shelf)}},
                                value=None,
                                on_change=lambda: handle_filter_shelf(query=query.value, state=state.value, genre=genre.value),
                                icon='book'
                            ).classes(remove="w-full", add="flex-1 sm:w-44")

                    with ui.column().classes('w-full overflow-y-auto grow pr-1'):
                        @ui.refreshable
                        def mini_render_shelf(user_shelf: list, max_results: int=6):
                            books_to_show = user_shelf[:max_results]

                            with ui.grid().classes('w-full grid-cols-2 sm:grid-cols-3 gap-4 md:gap-6 pb-6 pt-2 p-4'):
                                for user_book in books_to_show:
                                    user_book_card(
                                        user_book=user_book, 
                                        on_click=lambda bid=user_book.book_id: handle_add_to_top_shelf(user_id=user_id, book_id=bid, rank=rank)
                                    )

                        mini_render_shelf(user_shelf=user_shelf)
                        if initial_state:
                            handle_filter_shelf(state=initial_state)
                
    if on_close:
        dialog.on('hide', on_close)

    dialog.open()