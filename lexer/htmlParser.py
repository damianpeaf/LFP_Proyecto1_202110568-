import webbrowser


class HtmlParser():

    def __init__(self, documentStructure):
        self.documentStructure = documentStructure
        self.htmlStr = ""

    def createFile(self):
        self.createStr()

        try:

            file = open('./reports/RESULTADOS_202110568.html',
                        'w', encoding="utf-8")
            file.write(self.htmlStr)
            file.close()

            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open_new_tab(
                "file:///E:/U/SegundoAno2022/SegundoSemestre/LFP/PROYECTO_1/reports/RESULTADOS_202110568.html")

        except Exception as e:
            print(e)
            pass

    def createStr(self):
        self.htmlStr = f"""
<html>
    <head>
        <title>{self.createTitle()}</title>
    </head>
    <body>
        <header>
            <h1 style="{self.createStyles('ESTILOS_TITULO')}">{self.createTitle()}</h1>
            {self.createDescription()}
        </header>
        <main>
{self.createContent()}  
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
