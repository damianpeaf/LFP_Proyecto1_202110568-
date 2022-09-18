from typing import List
import webbrowser
from errors.LexicError import DocumentError

from lexer.lexer import Lexer


class HtmlParser2():

    def __init__(self):
        self.htmlStr = ""
        self.criticalErrors = Lexer.getCriticalErrors()
        self.tolerableErrors = Lexer.getTolerableErrors()

    def createFile(self):
        self.createStr()

        try:

            file = open('./reports/ERRORES_202110568.html',
                        'w', encoding="utf-8")
            file.write(self.htmlStr)
            file.close()

            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open_new_tab(
                "file:///E:/U/SegundoAno2022/SegundoSemestre/LFP/PROYECTO_1/reports/ERRORES_202110568.html")

        except Exception as e:
            print(e)
            pass

    def createStr(self):
        self.htmlStr = f"""
<html>
    <head>
        <title>ERRORES DEL ANALISIS LEXICO</title>
    </head>
    <body>
        <header>
            <h1>LISTA DE ERRORES</h1>
        </header>
        <main>
            <section>
                <h3>ERRORES PASABLES</h3>
                {
self.createErrorTable(self.tolerableErrors) if len(self.tolerableErrors) > 0 else "<p>No hay errores pasables</p>"
                }
            </section>
            <section>
                <h3>ERRORES CRITICOS</h3>
                {
self.createErrorTable(self.criticalErrors) if len(self.criticalErrors) > 0 else "<p>No hay errores criticos</p>"
                }
            </section>
        </main>
    </body>
</html>
"""
        return self.htmlStr

    def createTitle(self):
        titleStr = ""
        for word in self.documentStructure["TITULO"]:
            titleStr += str(word)
        return f"{titleStr}"

    def createDescription(self):
        descriptionStr = ""

        for line in self.documentStructure['DESCRIPCION']:
            descriptionStr += line
        return "<h1 style=\"" + self.createStyles('ESTILOS_DESCRIPCION') + f"\">{descriptionStr}</h1>"

    def createContent(self):

        contentStr = "\n"

        for line in self.documentStructure['CONTENIDO']:
            contentStr += f"\t\t\t<p style=\"" + \
                self.createStyles('ESTILOS_CONTENIDO') + f"\">{line}</p>\n"

        return contentStr

    def createStyles(self, tag):

        styles = ""
        for style in self.documentStructure[tag]:
            styles += style + " "

        return styles

    def createErrorTable(self, errors: List[DocumentError]):

        tableHeader = """
    <thead>
        <tr>
            <th>Numero de error</th>
            <th>Lexema</th>
            <th>Tipo</th>
            <th>Mensaje</th>
            <th>Fila</th>
            <th>Columna</th>
        </tr>
    </thead>
        """

        tableContent = "<tbody>"
        errorNumber = 0
        for error in errors:
            tableContent += f"""
    <tr>
        <td>{errorNumber}</td>
        <td>{error.lexeme}</td>
        <td>{error.type.name}</td>
        <td>{error.msg}</td>
        <td>{error.row}</td>
        <td>{error.column}</td>
    </tr>"""
        errorNumber += 1

        tableContent += "</tbody>"

        return f"<table border='1'>\n{tableHeader}\n{tableContent}\n</table>"
