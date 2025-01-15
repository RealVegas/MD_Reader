import os
import sys
import markdown
import re
from pathlib import Path
from tkinter.filedialog import askopenfile as ask_file


class MarkDownProcess:

    def __init__(self, file_name: Path) -> None:
        self.__file_name: Path = file_name
        self.__file_path: Path = Path(self.__file_name).parent
        self.__html_folder: str = Path(self.__file_name).parent.name
        self.__md_content: str
        self.__html_content: str
        self.__image_links: list[str]

    def __read_mark(self) -> str:
        self.__md_content: str = self.__file_name.read_text(encoding='utf-8')
        return self.__md_content

    def __get_html(self) -> str:
        self.__html_content: str = markdown.markdown(self.__md_content)
        return self.__html_content

    def __find_images(self) -> list[str]:
        self.__image_links: list[str] = re.findall(r'!\[.*?]\((.*?)\)', self.__md_content)
        return self.__image_links

    def __create_project(self) -> None:
        main_path: Path = Path(self.__html_folder)

        if not main_path.exists():
            main_path.mkdir(parents=True, exist_ok=True)
            if self.__find_images():
                image_folder: Path = Path(main_path, 'images')
                image_folder.mkdir(parents=True, exist_ok=True)

    def __save_html(self) -> Path:
        html_path: Path = Path(self.__html_folder, 'temp.html')
        html_path.write_text(self.__html_content, encoding='utf-8')

        return html_path

    def __copy_images(self) -> None:
        if not self.__find_images():
            return

        image_folder = Path(self.__html_folder, 'images')
        for one_link in self.__find_images():
            one_image: Path = Path(self.__file_path, one_link)
            os.system(f'copy {one_image} {image_folder} >nul 2>&1')  # Дополнительные параметры подавляют вывод сообщений

    def work(self) -> None:
        self.__read_mark()
        self.__get_html()
        self.__create_project()
        self.__copy_images()
        html_file = self.__save_html()

        os.startfile(html_file)


# Получение имени markdown-файла и пути к нему
def get_markdown(init_folder: Path) -> Path:
    md_name: str = ask_file(title='MD Reader v1.0 :: Выберите md-файл', filetypes=[('Markdown files', '*.md')],
                            defaultextension='.md', initialdir=init_folder).name

    if not md_name:
        print('В меню выбора файла была нажата кнопка "Отмена"')
        input('\nДля завершения программы нажмите Enter')
        sys.exit(1)

    return Path(md_name)


# Запуск программы
def main():
    markdown_name: Path = get_markdown(Path.cwd())

    markdown_handler = MarkDownProcess(markdown_name)
    markdown_handler.work()


if __name__ == "__main__":
    main()