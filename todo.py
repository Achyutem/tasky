import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todos, insert_todo, complete_todo, update_todo

console = Console()
app = typer.Typer()

@app.command(short_help='adds an item')
def add(task: str, category: str):
    typer.echo(f'adding {task}, {category}')
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command(short_help='delete an item')
def delete(position: int):
    typer.echo(f'deleting {position}')
    delete_todos(position-1)
    show()

@app.command(short_help='update an item')
def update(position: int, task: str, category: str):
    typer.echo(f'updating {position}')
    update_todo(position-1, task, category)
    show()

@app.command(short_help='checks an item')
def complete(position: int):
    typer.echo(f'complete {position}')
    complete_todo(position-1)
    show()

@app.command(short_help='shows the table')
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]TODOs[/bold magenta]!", "🖥️")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style='dim', width=6)
    table.add_column('Todo', min_width=20)
    table.add_column('Category', min_width=12, justify='right')
    table.add_column('Done', min_width=12, justify='right')

    def get_category_color(category):
        COLORS = {'Learn': 'magenta', 'Youtube': 'red', 'Sports': 'blue', 'Study': 'green', 'Grocery': 'red'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)

if __name__ == "__main__":
    app()

