from mkdocs_print_site_plugin.urls import fix_internal_links


class Renderer(object):
    def __init__(
        self, insert_toc=True, insert_explain_block=True, insert_full_urls=False
    ):
        """
        Args:
            insert_toc (bool): Insert a table of contents?
            insert_explain_block (bool): Insert a block explaining that this is a print page
        """

        self.insert_toc = insert_toc
        self.insert_explain_block = insert_explain_block
        self.insert_full_urls = insert_full_urls

        self.pages = []

    def write_combined(self):

        enabled_classes = []
        if self.insert_full_urls:
            enabled_classes.append("print-site-add-full-url")

        html = '<div id="print-site-page" class="%s">' % " ".join(enabled_classes)

        if self.insert_explain_block:
            html += self._explain_block()

        if self.insert_toc:
            html += self._toc()

        page_htmls = [fix_internal_links(p.html, p.url) for p in self.pages]
        html += "".join(page_htmls)

        html += "</div>"

        return html

    @staticmethod
    def _explain_block():
        return """
        <div id="print-site-banner">
            <p>
                <em>This box will disappear when printing</em>
                <span style="float: right"><a href="https://timvink.github.io/mkdocs-print-site-plugin/">mkdocs-print-site-plugin</a></span>
            </p>
            <p>This page combines all pages in the site. This makes it easy to print or export to PDF (<b>File > Print > Save as PDF</b>)</p>
        </div>
        """

    @staticmethod
    def _toc():
        return """
        <section class="print-page">
            <div id="print-page-toc"></div>
        </section>
        """

    @staticmethod
    def insert_css(html, file_path):
        css = (
            """
        <link href="%s" rel="stylesheet"> 
        """
            % file_path
        )
        return html.replace("</head>", css + "</head>")
